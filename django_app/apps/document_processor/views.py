"""
Document Processor Views
文件處理相關的視圖
"""
import logging
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.files.storage import default_storage

from .models import Document, ProcessingLog
from .serializers import DocumentSerializer, ProcessingLogSerializer
from .tasks import process_document_task

logger = logging.getLogger(__name__)


class DocumentViewSet(viewsets.ModelViewSet):
    """文件視圖集"""
    
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    
    @action(detail=False, methods=['post'])
    def upload(self, request):
        """
        上傳文件
        """
        try:
            file = request.FILES.get('file')
            if not file:
                return Response(
                    {"error": "未提供檔案"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 保存檔案
            file_path = default_storage.save(f'uploads/{file.name}', file)
            
            # 創建文件記錄
            document = Document.objects.create(
                document_id=f"DOC-{Document.objects.count() + 1:06d}",
                document_type=request.data.get('document_type', 'other'),
                file_name=file.name,
                file_path=file_path,
                file_size=file.size,
                uploaded_by=request.user if request.user.is_authenticated else None,
                status='uploaded'
            )
            
            # 觸發異步處理任務
            process_document_task.delay(document.id)
            
            serializer = self.get_serializer(document)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Error uploading document: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def processing_logs(self, request, pk=None):
        """
        取得文件的處理日誌
        """
        document = self.get_object()
        logs = document.logs.all()
        serializer = ProcessingLogSerializer(logs, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reprocess(self, request, pk=None):
        """
        重新處理文件
        """
        document = self.get_object()
        document.status = 'uploaded'
        document.error_message = None
        document.save()
        
        # 觸發異步處理任務
        process_document_task.delay(document.id)
        
        return Response({"message": "重新處理中"})
