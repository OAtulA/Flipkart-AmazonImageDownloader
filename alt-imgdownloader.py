from lxml import html
import os
import requests
import asyncio
from playwright.async_api import async_playwright

# This is literally going to download the pics
def downLoading(product, images, bigImage, Pic_name, url, OutputLocation):

    # This code is mainly going to grab the image
    image_count = 1
    # So that even if we have multiple images for
    # same product we can easily choose.    

    bigImageLink = bigImage.xpath('@src')[0]

    if product.strip() != '':
        for image in images:
            name = Pic_name + " " + str(image_count)
            image_count += 1
            # to get all the images of a product

            # link = image['src']
            link = image.xpath('@src')[0]
            

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
                bigDimension = bigImageLink[start_index:end_index]
                
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



def download_image(name, link, OutputLocation):

    name = name.replace(' ', '-').replace('/', '') + '.jpg'
    name = os.path.join(OutputLocation, name)
    with open(name, 'wb') as photo:
        im = requests.get(link)
        photo.write(im.content)
        print('Writing:', name)

async def scrape_website(product, url, Pic_name, OutputLocation):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)

        # Wait for the page to reach the load state
        await page.wait_for_load_state()

        html_content = await page.content()

        html_tree = html.fromstring(html_content)
        images = html_tree.xpath("//ul[@class='_3GnUWp']/li/div/div/img")
        bigImage = html_tree.xpath("//div[@class='_1BweB8']")
        # bigImage = html_tree.xpath("//div[@class='_1BweB8']//img")

        # download_image(Pic_name, bigImage[0].xpath('@src')[0], OutputLocation)
        downLoading(product= product, images= images, bigImage= bigImage, Pic_name= Pic_name, url= url, OutputLocation= OutputLocation)

        await browser.close()

async def img_graber(products, OutputLocation):
    for product in products:
        Pic_name, link = product.split(',')
        Pic_name = Pic_name.strip()
        link = link.strip()
        url = link

        if 'flipkart' in url:
            await scrape_website(product, url, Pic_name, OutputLocation)
        # You can add support for other websites as needed.

def Inputs():
    file = open('Inputfile', 'r')

    InputLines = []
    temp_inputLines = file.readlines()

    for line in temp_inputLines:
        if line != '\n':
            InputLines.append(line.strip('\n'))

    for i in range(len(InputLines)):
        if "Products File:" in InputLines[i]:
            productsInfo = open(InputLines[i+1], 'r')
            products = productsInfo.readlines()
            productsInfo.close()
        elif "Image Output Folder:" in InputLines[i]:
            OutputLocation = InputLines[i+1]
            try:
                os.makedirs(OutputLocation)
            except:
                pass

    temp_products = products
    products = []

    for p in temp_products:
        p = p.strip('\n')

        if p != '':
            products.append(p)

    asyncio.run(img_graber(products=products, OutputLocation=OutputLocation))
    file.close()

Inputs()
