import PyPDF2
import struct

from PIL import Image
import base64
from io import BytesIO
import cStringIO
from openerp.osv import osv


import sys
from os import path
import warnings
warnings.filterwarnings("ignore")

number = 0
def pdfOrTiff2image(modelo,filedataByte,contenedor):
    file = None
    try:
        file = PyPDF2.PdfFileReader(filedataByte)
        for p in range(file.getNumPages()):    
            page0 = file.getPage(p)
            # print page0
            jpeg_image_buffer = recurse(p, page0)
            imgStr = base64.b64encode(jpeg_image_buffer.getvalue())
            #raise osv.except_osv('Esto es un Mesaje!',repr(im.info))
            contenedor.imagenes_ids |= modelo.env['rbs.imagenes'].create({'imagen': imgStr,'contenedor_id':contenedor.id,"posicion":p})
    except:
        im = Image.open(filedataByte)
        
        n = 0
        # modelo.contenedor_id=contenedor.id
        while True:
            try:
                n = n+1
                im.seek(n)
                #im.save('Block_%s.tif'%(n,))

                jpeg_image_buffer = cStringIO.StringIO()
                im.save(jpeg_image_buffer, format="PNG")
                imgStr = base64.b64encode(jpeg_image_buffer.getvalue())
                contenedor.imagenes_ids |= modelo.env['rbs.imagenes'].create({'imagen': imgStr,'contenedor_id':contenedor.id,"posicion":n-1})
                #raise osv.except_osv('Esto es un Mesaje!',imgStr)
            except EOFError:
                print "Se Cargo la imagen tiff",  n
                break;
        return



    print('%s extracted images'% number)
def tiff_header_for_CCITT(width, height, img_size, CCITT_group=4):
    tiff_header_struct = '<' + '2s' + 'h' + 'l' + 'h' + 'hhll' * 8 + 'h'
    return struct.pack(tiff_header_struct,
                       b'II',  # Byte order indication: Little indian
                       42,  # Version number (always 42)
                       8,  # Offset to first IFD
                       8,  # Number of tags in IFD
                       256, 4, 1, width,  # ImageWidth, LONG, 1, width
                       257, 4, 1, height,  # ImageLength, LONG, 1, lenght
                       258, 3, 1, 1,  # BitsPerSample, SHORT, 1, 1
                       259, 3, 1, CCITT_group,  # Compression, SHORT, 1, 4 = CCITT Group 4 fax encoding
                       262, 3, 1, 0,  # Threshholding, SHORT, 1, 0 = WhiteIsZero
                       273, 4, 1, struct.calcsize(tiff_header_struct),  # StripOffsets, LONG, 1, len of header
                       278, 4, 1, height,  # RowsPerStrip, LONG, 1, lenght
                       279, 4, 1, img_size,  # StripByteCounts, LONG, 1, size of image
                       0  # last IFD
                       )
def recurse(page, xObject):
    global number

    # xObject = xObject['/Resources']['/XObject'].getObject()
    # print xObject['/Resources']
    xObject = xObject['/Resources']['/XObject'].getObject()
    jpeg_image_buffer = cStringIO.StringIO()
    for obj in xObject:
        
        if xObject[obj]['/Subtype'] == '/Image':
            # print xObject[obj]['/Filter']
            size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
            data = xObject[obj]._data
            if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                mode = "RGB"
            else:
                mode = "P"
            
            # imagename = "%s - p. %s - %s"%(abspath[:-4], p, obj[1:])

            if xObject[obj]['/Filter'][0] == '/FlateDecode':
                print "FlateDecode"

                img = Image.open(BytesIO((data)))
                img.save(jpeg_image_buffer, format="PNG")
                number += 1
            elif xObject[obj]['/Filter'][0] == '/DCTDecode':
                print "DCTDecode"

                img = Image.open(BytesIO((data)))
                img.save(jpeg_image_buffer, format="PNG")
                number += 1
            elif xObject[obj]['/Filter'][0] == '/JPXDecode':
                print "JPXDecode"
                # img = open(imagename + ".jp2", "wb")
                img = Image.open(BytesIO((data)))
                img.save(jpeg_image_buffer, format="PNG")
                number += 1
            elif xObject[obj]['/Filter'][0] == '/CCITTFaxDecode':
                print "CCITTFaxDecode"
                # print xObject[obj]['/DecodeParms'][0]["/K"]
                if xObject[obj]['/DecodeParms'][0]['/K'] == -1:
                    CCITT_group = 4
                else:
                    CCITT_group = 3
                width = xObject[obj]['/Width']
                height = xObject[obj]['/Height']
                data = xObject[obj]._data  # sorry, getData() does not work for CCITTFaxDecode
                img_size = len(data)
                tiff_header = tiff_header_for_CCITT(width, height, img_size, CCITT_group)


                img = Image.open(BytesIO((tiff_header + data)))
                img.save(jpeg_image_buffer, format="PNG")
                # img.save(imagename+".png", format="PNG")
                number += 1
            else:
                raise osv.except_osv('Incompatible!',"Formato no compatible"+xObject[obj]['/Filter'][0])

            return jpeg_image_buffer
        else:
            recurse(page, xObject[obj])

try:
    filename = "C:\\Users\\adria\\Downloads\\PyPDF2-master\\PyPDF2-master\\Sample_Code\\pdf.pdf"
    abspath = path.abspath(filename)
except BaseException:

    print('Usage :\nPDF_extract_images file.pdf page1 page2 page3 ')
    sys.exit()


