You will build a portible application to change a users game server for the game rainbow six siege. The application will be in the form of a .exe, that is portible, allowing anyone to download and use. 

When the application opens, the user will be asked for the ubisoft name of the account that they are trying to change and then the user will select (from a GUI) their desired server from this list of options:
    Default
    US-West
    US-Central
    US-South-Central
    East-US
    Brazil
    EU-North
    EU-West
    UAE
    South Africa
    Asia-East
    Asia-Southeast
    Japan
    Australia

The reason that we must acquire the users ubisoft name, is because in order to change the game server, we must identify their ubisoft ID as the gamesettings.ini file is located under "C:\Users\Elliott\OneDrive\Documents\My Games\Rainbow Six - Siege\[ACCOUNT-UBISOFT-ID]\gamesettings.ini"

As an alternative to providing a username, the user should have an option to skip this step, resulting in the server being changed for ALL gamesettings.ini under ../My Games/Rainbow Six - Siege/

## ACQUIRING UBISOFT ID FROM UBISOFT USERNAME:
    To acquire the ubisoft ID of the account the user specified, we can navigate to the URL:

        https://stats.cc/siege

        Once on this page, we can enter the users ubisoft username into the search bar (SEARCH-BOX-FULLXPATH) and it will take us to the page "https://stats.cc/siege/[UBISOFT_USERNAME]/[UBISOFT_ID]"
        from this page, we can grab the users ubisoft ID from the URL 

    SEARCH-BOX-FULLXPATH=/html/body/div[1]/div[1]/div/div[2]/div[2]/main/div/div/div[1]/div[2]/input
    



## LOCATING ACCOUNT GAMESETTINGS.INI

    In order to change the users server, we must locate the users "gamesettings.ini" file for the specified account. 
    The gamesettings.ini folder will be in either "C:\Users\<User>\Documents\My Games\Rainbow Six - Siege\<UBISOFT-ID>\GameSettings.ini" or "C:\Users\<User>\OneDrive\Documents\My Games\Rainbow Six - Siege\<UBISOFT-ID\GameSettings.ini". We can identify the specified folder using the ubisoft ID we acquired earlier. 


## CHANGING THE USERS SERVER
    To change the users server, you will open the gamesettings.ini file and look for the variable "DataCenterHint=" and assign it to one of the following options:
        default
        playfab/australiaeast
        playfab/brazilsouth
        playfab/centralus
        playfab/eastasia
        playfab/eastus
        playfab/japaneast
        playfab/northeurope
        playfab/southafricanorth
        playfab/southcentralus
        playfab/southeastasia
        playfab/uaenorth
        playfab/westeurope
        playfab/westus
    examples:
        DataCenterHint=default
        DataCenterHint=playfab/westus
    After changing the users server to their requested


## DESIGN
    The GUI design should be clean and nice looking, but lightweight to ensure that the application opens as quick as possible



