import requests
from bs4 import BeautifulSoup
from google.oauth2 import service_account #using googlesheets api
from googleapiclient.discovery import build #using googlesheetsid




print("Script is running with beautiful soup!")


def getLinksFromWebPage(url) :
    #if multiple links, transform this into a for loop that does repetitive action
    response = requests.get(url).text
    print( response)
    soup = BeautifulSoup(response, 'html.parser') ## blob of content 

    links = []
    ##make a for loop to Get All links
    for link in soup.find_all('a'): #try without quotes
        linkString = link.get('href')
        if linkString is None:
            continue
        if "#" in linkString :
             continue
        if "about-us" in linkString : 
             continue
    
        if "click-to-help" in linkString:
            continue
        if "donate" in linkString : 
            links.append(linkString)


    for link in links:
        print("Link found : ")
        print(link)
    
    return links
   

# Debug Bad Request Error

def writeUrlsToSpreadsheet(urllist: list[str]):
   
        # set important spreadsheet/file location vars
    SPREADSHEET = "1Ydvr5He59QNhzNqy4ZBOkeRHiH_qsiCEulOdTOJk9uA"
    credentials =  service_account.Credentials.from_service_account_file(
    'starlit-casing-422716-g6-265738d36a69.json')

    try: 
        # build a service object for the API 
        service = build("sheets", "v4", credentials=credentials)
        print("Built credentials, service and now writing links to spreadsheet")
        urlLen = len(urllist)

        #Specify range to write values (column A) 
        range_urls = '{}!A2:A{}'.format("Donations", urlLen+1)
        
        print("Created range-urls, proceeding to define values to spreadsheet")
    
        # Define the values to be written to the spreadsheet
        values = [[url] for url in urllist]

        #Specify content to write to spreadsheet
        body = {'values' : values}

        print("About to make api request call")
        # Make request to write urls to spreadsheet
        rowsResult = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET,
            valueInputOption= 'RAW',
            range = range_urls,
            body = body
        ).execute()

        # Print num of cells Updated post call
        print("Cells updated:", rowsResult.get('updatedCells'))
       
        

    except Exception as e:
        print("Error occurred while trying to reach API:", e)

    
   

   


def main() :
 
    links = getLinksFromWebPage("https://arab.org/portal/palestine/where-to-donate/")

    writeUrlsToSpreadsheet(links)
 

    


if __name__ == "__main__":
    main()

