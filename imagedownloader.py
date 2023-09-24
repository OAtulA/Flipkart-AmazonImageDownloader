from lxml import html
import requests
# from bs4 import BeautifulSoup
import os

# url = 'https://www.airbnb.co.uk/s/Ljubljana--Slovenia/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&query=Ljubljana%2C%20Slovenia&place_id=ChIJ0YaYlvUxZUcRIOw_ghz4AAQ&checkin=2020-11-01&checkout=2020-11-08&source=structured_search_input_header&search_type=autocomplete_click'

# This is literally going to download the pics
def downlloading(product, images, bigImage, Pic_name, url, OutputLocation):

    # This code is mainly going to grab the image
    image_count = 1
    # So that even if we have multiple images for
    # same product we can easily choose.    

    if product.strip() != '':
        for image in images:
            name = Pic_name + " " + str(image_count)
            image_count += 1
            # to get all the images of a product

            # link = image['src']
            link = image.xpath('@src')[0]
            bigImageLink = bigImage.xpath('@src')[0]

            # Link looks like this 
            '''
            # 1st small image 
            # src="https://rukminim2.flixcart.com/image/128/128/xif0q/shoe/l/t/l/8-rkt-19039-black-42-atom-black-original-imagzmhf7d8fgd38.jpeg?q=70"

            # 1st big image 
            # src="https://rukminim2.flixcart.com/image/832/832/xif0q/shoe/l/t/l/8-rkt-19039-black-42-atom-black-original-imagzmhf7d8fgd38.jpeg?q=70"
            '''

               # Now setting the link to get the big images for flipkart
            if 'flipkart' in url:
                # Now I get the smallImage dimesions as well as big images dimensions.
                start_index = link.find("image/") + len("image/")
                end_index = start_index + 7
                smallDimension = link[start_index:end_index]

                start_index = bigImageLink.find("image/") + len("image/")
                end_index = start_index + 7
                bigDimension = link[start_index:end_index]

                link = link.replace(smallDimension, bigDimension)

                # Not needed now.
                # link = link.replace('q=70', 'q=50')

            name = name.replace(' ', '-').replace('/', '') + '.jpg'
            name = OutputLocation + '/' + name
            # To get the file in the desired location

            with open(name, 'wb') as photo:
                im = requests.get(link)
                photo.write(im.content)
                # Writing the downloaded file.
                print('Writing: ', name)


# I have put the site specific customisation in img_graber()
def img_graber(products, OutputLocation):
    
    for product in products:
        # As the data format is <Product Name>, <Product Link>
        Pic_name, link = product.split(',')
        Pic_name = Pic_name.strip()
        link = link.strip()
        url = link
        response = requests.get(url)
        # soup = BeautifulSoup(response.text, 'html.parser')
        # I think soup is not needed

        html_tree = html.fromstring(response.content)
        #  This has the html content

        # images = soup.find_all('img')

        # Here Appropriate xpath or css selector will be given
        # So as to only select images of the given product.
        if 'flipkart' in url:
            # images = html_tree.xpath('//*[@id="mw-content-text"]/div/table[2]/tbody/tr[*]/th/i/a')
            images = html_tree.xpath("//ul[@class='_3GnUWp']/li/div/div/img")            
            bigImage = html_tree.xpath("//div[@class='_1BweB8']//img")

            #  Removing amazon support for now. Will do it later.
            #  If I wish :)
        # elif 'amazon' in url:
        #     # Getting the images of products from amazon
        #     images2 = html_tree.xpath("//div[@id='altImages']/ul/li")
        #     images = images2.xpath("//img")

    downlloading(product= product, images= images, bigImage= bigImage, Pic_name= Pic_name, url=url, OutputLocation= OutputLocation)
    # def downlloading(product, images, Pic_name, url, OutputLocation):


def Inputs():
    file = open('Inputfile', 'r')

    InputLines = []
    temp_inputLines = file.readlines()

    for line in temp_inputLines:
        if line != '\n':
            InputLines.append(line.strip('\n'))

    # productsInfo = ""
    # OutputLocation = ""

    # To get the products file and Output location.
    for i in range(len(InputLines)):
        # if InputLines[i] == "Products File:" :
        if "Products File:" in InputLines[i]:
            productsInfo = open(InputLines[i+1], 'r')

            products = productsInfo.readlines()
            # THis contains the main content of the products file
            productsInfo.close()

        # elif InputLines[i] ==  "Image Output Folder:" :
        elif "Image Output Folder:" in InputLines[i]:
            OutputLocation = InputLines[i+1]
            # This is the output Location.
            try:
                os.makedirs(OutputLocation)
                # It will create the output folder.
                # If it doesn't exist.
            except:
                pass

    # TO remove all the \n from products
    temp_products = products
    products = []

    for p in temp_products:
        p = p.strip('\n')

        if p != '':
            products.append(p)

    img_graber(products=products, OutputLocation=OutputLocation)

    file.close()

Inputs()

# THe below lines might have been for testing something.
# def imagedown(url, folder):
#     try:
#         os.mkdir(os.path.join(os.getcwd(), folder))
#     except:
#         pass
#     os.chdir(os.path.join(os.getcwd(), folder))
#     r = requests.get(url)
#     soup = BeautifulSoup(r.text, 'html.parser')
#     images = soup.find_all('img')
#     for image in images:
#         name = image['alt']
#         link = image['src']
#         with open(name.replace(' ', '-').replace('/', '') + '.jpg', 'wb') as f:
#             im = requests.get(link)
#             f.write(im.content)
#             print('Writing: ', name)

# imagedown('https://www.airbnb.co.uk/s/Bratislava--Slovakia/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&place_id=ChIJl2HKCjaJbEcRaEOI_YKbH2M&query=Bratislava%2C%20Slovakia&checkin=2020-11-01&checkout=2020-11-22&source=search_blocks_selector_p1_flow&search_type=search_query', 'bratislava')
