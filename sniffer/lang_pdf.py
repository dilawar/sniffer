from cStringIO import StringIO
import pdf2text

class Pdf:
  def __init__(self) : pass
  
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

