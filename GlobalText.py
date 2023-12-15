
bgp_ASCII_INTRO = """
                   ______   _______  _______         _______ _________ _______ 
                  (  ___ \ (  ____ \(  ____ )       (  ____ \\__   __/(       )
                  | (   ) )| (    \/| (    )|       | (    \/   ) (   | () () |
                  | (__/ / | |      | (____)| _____ | (_____    | |   | || || |
                  |  __ (  | | ____ |  _____)(_____)(_____  )   | |   | |(_)| |
                  | (  \ \ | | \_  )| (                   ) |   | |   | |   | |
                  | )___) )| (___) || )             /\____) |___) (___| )   ( |
                  |/ \___/ (_______)|/              \_______)\_______/|/     \|

    ###########################################################################################
    #                                *DEFAULT CONNECTIONS*                                    #
    #                 _______                 _______                 _______                 #
    #                /       \               /       \               /       \                #
    #               |   AS2   |-------------|   AS4   |-------------|   AS9   |               #
    #                \_______/               \_______/               \_______/                #
    #               /                                                                         #
    #     _______  /              _______                 _______                 _______     #
    #    /       \/              /       \               /       \               /       \    #
    #   |   AS1   |-------------|   AS7   |             |   AS5   |-------------|   AS10  |   #
    #    \_______/\              \_______/               \_______/               \_______/    #
    #              \                                    /                                     #
    #               \ _______                 _______  /                                      #
    #                /       \               /       \/                                       #
    #               |   AS3   |-------------|   AS6   |                                       #
    #                \_______/               \_______/\                                       #
    #                                                  \                                      #
    #                                                   \ _______                             #
    #                                                    /       \                            #
    #                                                   |   AS8   |                           #
    #                                                    \_______/                            #
    #                                                                                         #
    #                                 *DEFAULT CONNECTIONS*                                   #
    ###########################################################################################
    Project for the PPaS course, created by MarkLeppi, Eikrt, and Uteeaami.
    """

bgp_usage = """
    BGP-Simulator, created for the Protocol Processing and Security course @ University of Turku.
    Main flow and usage of the project:
        - Scroll up to see default configurations for the routers
        - Keep the original configuration, by pressing 'enter' or add new connections
        - !NOTE! If any router doesn't have a connection, the original config will be used on top
        - Router connections are added by referencing the routers name. In total there are 10 routers, so router.name = (r1, r2, r3, r..., r10)
        - ADDING CONNECTIONS
            : FLOW
                : type: router.name -> press 'enter' -> type: router.name
            : EXAMPLE BELOW
                : Connect router (or 'enter' to continue): r1
                : 'ENTER'
                : To: r6
                : 'ENTER'
        - The configuration takes around ~60 seconds, so wait patiently until no new updates are received
        - To get to printing the routing tables, press 'ENTER'
        -PRINTING ROUTINGTRABLE
            : type: router.name -> press 'ENTER'
            : EXAMPLE BELOW
                : Print routingtable of router: r1
                : 'ENTER'
                : 'ENTER' -> (To be able to print a new routing table (step 1 of this example))
"""