from cStringIO import StringIO
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.layout import LAParams

class Pdf:

    def __init__(self):
        self.password = None
        self.codec = 'utf-8'

    def getPDFContent(self, path):
          try:
              import pyPdf
              content = ""
              # Load PDF into pyPDF
              pdf = pyPdf.PdfFileReader(file(path, "rb"))
              # Iterate pages
              for i in range(0, pdf.getNumPages()):
                  # Extract text from page and add to content
                  content += pdf.getPage(i).extractText() + "\n"
                  # Collapse whitespace
                  content = " ".join(content.replace(u"\xa0", " ").strip().split())
              return content
          except Exception as e:
              print("[ERROR] Failed to convert pdf to text. Tried methods : pdftotext"\
                  + " pdfminer libary and pyPdf libary ..")
              return ""


    def fix_text(self, filename):
        # Open a PDF file.
        pdfText = StringIO()
        fp = open(filename, 'rb')
        # Create a PDF parser object associated with the file object.
        parser = PDFParser(fp)
        # Create a PDF document object that stores the document structure.
        # Supply the password for initialization.
        if not self.password:
            document = PDFDocument(parser)
        else:
            document = PDFDocument(parser, self.password)
        # Check if the document allows text extraction. If not, abort.
        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed
        # Create a PDF resource manager object that stores shared resources.
        rsrcmgr = PDFResourceManager()
        # Create a PDF device object.
        device = TextConverter(rsrcmgr, pdfText, codec=self.codec
                , laparams=LAParams(), imagewriter=None
                )
        # Create a PDF interpreter object.
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        # Process each page contained in the document.
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
        txt = pdfText.getvalue()
        return txt

