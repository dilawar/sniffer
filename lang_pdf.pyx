from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from cStringIO import StringIO

class Pdf :
  def __init__(self) : pass

  def fix_text_tem(self, path, lang_type):
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
    retstr.close()
    return str, 50

#  def getPDFContent(self, path):
#      import pyPdf
#      content = ""
#      # Load PDF into pyPDF
#      pdf = pyPdf.PdfFileReader(file(path, "rb"))
#      # Iterate pages
#      for i in range(0, pdf.getNumPages()):
#          # Extract text from page and add to content
#          content += pdf.getPage(i).extractText() + "\n"
#          # Collapse whitespace
#          content = " ".join(content.replace(u"\xa0", " ").strip().split())
#      return content
#
  def fix_text(self, file, lang_type) :
    try :
      process_text = self.getPDFContent(file).encode("ascii", "ignore")
      line = 50
      return process_text, line
    except AttributeError :
      print "Attribute error."


