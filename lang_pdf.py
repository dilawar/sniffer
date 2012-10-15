import pyPdf
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO

class Pdf :
  def __init__(self) : pass

  def parse_lt_objs (lt_objs, page_number, images_folder, text=[]):
    """Iterate through the list of LT* objects and capture the text or image data contained in each"""
    text_content = []

    page_text = {} # k=(x0, x1) of the bbox, v=list of text strings within that bbox width (physical column)
    for lt_obj in lt_objs:
        if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
            # text, so arrange is logically based on its column width
            page_text = update_page_text_hash(page_text, lt_obj)
    for k, v in sorted([(key,value) for (key,value) in page_text.items()]):
        # sort the page_text hash by the keys (x0,x1 values of the bbox),
        # which produces a top-down, left-to-right sequence of related columns
        text_content.append(''.join(v))

    return '\n'.join(text_content)


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

  def getPDFContent(self, path):
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

  def fix_text(self, file, lang_type) :
    try :
      process_text = self.getPDFContent(file).encode("ascii", "ignore")
      line = 50
      return process_text, line
    except AttributeError :
      print "Attribute error."


