import requests
import os
from PIL import Image
from docx import Document
from docx2pdf import convert

## THIS FUNCTION GENERATES A NEW REVIEW FOR SIMPLE HTML WEBSITE ##

def generate_new_review():

## SCRAPE THE WEBSITE TO GET THE CODE OF THE WEBSITE ##
    main_url = 'http://mikesflix.com'
    request = requests.get(main_url)
    # had to change the encoding to work
    request.encoding = request.apparent_encoding
    page_source = request.text
    page_source = request.text.replace('\r',"")

    ## GRABS THE LOCATION OF WHERE THE NEW REVIEW WILL BE ENTERED WITHIN THE PAGE SOURCE ##
    start_page_source = page_source[:page_source.find("<!--Review Start-->")]
    end_page_source = page_source[page_source.find("<!--Review Start-->"):]

    ## ESTABLISHING VARIABLES USED LATER ON ##
    paragraph_with_p = "</p>\n<p>"
    rating_runtime = ""
    
    ## GETS PATH TO THE PDF FORMATTED REVIEW ##
    path_to_docx = input("Enter .docx full path: ")
    full_image_path = input("Enter full image path: ")
    photo_credit = input("Photo credit from email: ")

    # GETS THE RIGHT EXTENSIONS FOR FORMATTING
    docx_extension = os.path.basename(path_to_docx)
    pdf_name = os.path.splitext(docx_extension)[0]

    # FORMATS FILE/IMAGES NAMES
    image_path = os.path.basename(full_image_path)
    resize_image_name = f'{os.path.splitext(image_path)[0]}-resized{os.path.splitext(image_path)[1]}'
    sidebar_image_name = f'{os.path.splitext(image_path)[0]}-sidebar{os.path.splitext(image_path)[1]}'

    # EDITS THE IMAGE TO THE CORRECT SIZE
    with Image.open(full_image_path) as im:
        

        resized_image = im.resize((int((430 / im.width)*im.width), int((430 / im.width)*im.height)))
        sidebar_image = im.resize((int((125 / im.width)*im.width), int((125 / im.width)*im.height)))
        # resized_image = im.resize((430,230))
        # sidebar_image = im.resize((125,70))
        # print(resized_image.size)
        # print(sidebar_image.size)
        
        # resized_image = im.resize((430,230))
        # sidebar_image = im.resize((125,70))
        resized_image.save(resize_image_name)
        sidebar_image.save(sidebar_image_name)
        

    # READS THROUGH file.DOCX TO GET PARAGRAPHS AND ADDS EACH PARAGRAPH TO AN ARRAY
    doc = Document(path_to_docx)
    text_array = []
    for paragraph in doc.paragraphs:
        text_array.append(paragraph.text)
 
    # REMOVES PARAGRAPHS THAT ARE EMPTY STRINGS
    text_array = [text for text in text_array if text != '']
    month_year = text_array[-1]
    rating_runtime = text_array[-2]
    rest_of_review = paragraph_with_p.join(text_array[2:-2])

    # CONVERTS file.docx TO file.pdf AND SAVES TO SAME FOLDER YOU SAVED file.docx
    convert(path_to_docx, f"{pdf_name}.pdf")

    # LATEST REVIEW SETUP
    full_review = "<!--Review Start-->\n<!--Movie Title--><b><font size=\"+2\">" + text_array[0] +  "</font></b><br><br>\n<!--First paragraph--><big>" + text_array[1] + "<br><br>\n<!--Resized Image--><img src=\"images/" + resize_image_name +"\" alt=\"\" width=\"430\"><br><br>\n <!--Photo Credit--> <strong>" + photo_credit + "</strong><br><br>\n<!--Rest of review-->\n<p>" + rest_of_review + "</p>\n <!--Rating and Runtime--><i>" + rating_runtime + "</i><br><br>\n <!--Month and year-->" + month_year +"</big><br><br> \n<!--Review End-->"

    ## ADDS THE NEWLY GENERATED CODE THE PAGE SOURCE AND GENERATES NEW FILE TO VIEW FOR EDITTING ##
    new_code = start_page_source + full_review + end_page_source
    f = open("newindex.html", "w", encoding='utf-8')
    
    f.write(new_code)
    f.close()

generate_new_review()