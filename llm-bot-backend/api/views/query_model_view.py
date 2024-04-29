from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.decorator import route_permissions
from api.parsers import MultipartJsonParser
from api.models import Document, Log, Message, Session, Document
import ollama
from django.db import IntegrityError, transaction
from openai import OpenAI
import fitz
import cv2
import pytesseract
import requests
import time
import numpy as np
from api.serializers import DocumentSerializer
import os
from django.conf import settings

class QueryModelView(APIView):

    permission_classes = (IsAuthenticated, )
    parser_classes = (MultipartJsonParser, )

    # @route_permissions(['query_gpt'])
    def post(self, request):
        data = request.data
        message = None
        if 'message' in data:
            message = data['message']
        documents = data['files']
        file = None
        if 'file' in  documents:
            file = documents['file']
        new_session = False
        session_obj = None

        # pytesseract.pytesseract.tesseract_cmd =r'C:/Program Files/Tesseract-OCR/tesseract.exe'

        try:
            with transaction.atomic():

                if 'new_session' in data:
                    new_session = True
                    session_obj = Session.objects.create(user=request.user)
                elif 'session' in data:
                    session = data['session']
                    try:
                        session_obj = Session.objects.get(id=session)
                    except Session.DoesNotExist:
                        return Response(status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

                document = None
                document_string = None
                if file:
                    document = Document.objects.create(name=file.name, path=file)
                    document_data = DocumentSerializer(document).data
                    relative_path_arr = document_data['path'].split('/')
                    doc_path = os.path.join(os.getcwd(), *relative_path_arr)
                    # document_string = process_pdf_and_return_file_contents(doc_path)
                    document_string = pdf_to_text(doc_path)
                    message = 'These are the contents extracted from a file. Please explain. Also hide sensitive information unless explicity asked for. ' + document_string

                # docs = []
                # for (key, value) in documents.items():
                #     docs.append(doc)
                # print(docs[0])

                messages = []
                # if new_session:
                #     messages = [
                #         {
                #             'role': 'system',
                #             'content': 'You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature',
                #         },        
                #     ]

                # if new_session:
                #     Message.objects.create(
                #         message_type = Message.TYPE_TEXT,
                #         session = session_obj,
                #         role = 'system',
                #         content = 'You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature',
                #         user = request.user,
                #     )


                if document:
                    message_type = Message.TYPE_DOCUMENT
                else:
                    message_type = Message.TYPE_TEXT
                Message.objects.create(
                    message_type = message_type,
                    session = session_obj,
                    role = 'user',
                    content = message,
                    document = document
                )


                messages = list(session_obj.messages.all().values('role','content'))


                # FOR LLAMA 3 WITH OLLAMA
                # response = ollama.chat(model='llama3', messages=messages)
                # print(response['message']['content'])
                # message_content = response['message']['content']

                #FOR CHAT GPT WITH OPEN AI API
                openai_api_key = settings.OPENAI_API_KEY
                client = OpenAI(api_key=openai_api_key)
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                )
                message_content = response.choices[0].message.content

                Message.objects.create(
                    message_type = Message.TYPE_TEXT,
                    session = session_obj,
                    role = 'assistant',
                    content = message_content,
                )
                print('OK')

                messages = list(session_obj.messages.all().values('role','content', 'message_type','document'))

                print(messages)

                response_data = {
                    'session': session_obj.id,
                    'messages': messages
                }

        except IntegrityError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)  

        return Response(status=status.HTTP_200_OK, data=response_data)


def pdf_to_text(pdf_path):
    doc = fitz.open(pdf_path)
    images = []
    extracted_string = ''
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        tabs = page.find_tables()

        for tab in tabs:
            page.add_redact_annot(tab.bbox)
        page.apply_redactions()

        remaining_image = page.get_pixmap(dpi=500)

        img_array = np.frombuffer(remaining_image.samples, dtype=np.uint8).reshape((remaining_image.height, remaining_image.width, 3))[:, :, :3]

        gray_image = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray_image)
        extracted_string += text.strip() + ' \n ' + ' - ' + ' \n '
        remaining_image = None
        img_array = None
        gray_image = None
        text = None
        page = None
        
    doc.close()
    doc = None
    doc = fitz.open(pdf_path)
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        tabs = page.find_tables()
        for tab in tabs:
            for cell in tab.cells:
                page.set_cropbox(cell)
                cell_image = page.get_pixmap(dpi=500)
                img_array = np.frombuffer(cell_image.samples, dtype=np.uint8).reshape((cell_image.height, cell_image.width, 3))[:, :, :3]
                gray_image = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
                text = pytesseract.image_to_string(gray_image)
                extracted_string += text + ' \n ' + ' - ' + ' \n '
    doc.close()

    return extracted_string