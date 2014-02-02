from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO

class Pdf:
  def __init__(self) : pass
  
  def getPdfText(self, path):
    try:
      rsrcmgr = PDFResourceManager()
      retstr = StringIO()
      codec = 'utf-8'
      laparams = LAParams()
      device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
      fp = file(path, 'rb')
      process_pdf(rsrcmgr, device, fp)
      fp.close()
      device.close()
      str = retstr.getvalue()
    except Exception as e:
      return self.getPDFContent(path)
    else:
      retstr.close()
      return str

  def fix_text(self, path):
    txt = ""
    # Using pdftotext program to convert pdf to text
    import subprocess 
    try:
      txt = subprocess.check_output(["pdftotext", path, "-"]
          , stderr=subprocess.PIPE
          )
    except Exception as e:
      return self.getPdfText(path)
    txt = txt.split("\n")
    return "".join(txt)


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

