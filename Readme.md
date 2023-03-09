

# Marvel REST API Challenge

## Index
- [Design](#design)
- [Run](#run)
- [Tests](#tests)
- [Endpoints](#endpoints)
- [Improvements](#improvements)

## Techs
- Django v3.2.18
- djangorestframework v3.14.0
- mysql v8.0
 
## Design
- `marvelAPI.py` class for handling the connection with the [Marvel API](https://developer.marvel.com/), it makes requests to different endpoints and formats the information recieved by the endpoints.

    - **build_url_and_get_results** constructs an URL base on the parameters needed, such as ts, publick key and hash required by the marvel APi, besides to query to a resource (depending on the case) to get certain information, and makes the request to the URL constructed.
        - Parameters 
                *query* (required, string): endpoint with its require parameters to be consulted.
        - Returns 
                *results* (list), results obtained by the request.
    - **get_img_urls_and_info_from_object** gets image imformation from a dict.
        - Parameters 
                *thumbnail* (required, dict): dict with image propertils which path and extension.
        - Returns 
                *image path* (string), path of the image including the name of the file.
                *image extension* (string), extension of the image.
                *image full url* (string), full path of the image including extension.
    - **format_characters_and_ids** extracts to information for a list and formats each character to be stored on the DB.
        - Parameters 
                *characters* (required, list): list of the characters to be formatted.
                *id_comic* (optional, integer): id of a comic, used to know if a character is or not already related to a comic.
                *character_model* (required, ModelBase): character model.
                *charactercomic_model* (required, ModelBase): charactercomic model.
        - Returns
                *characters_list* (list) characters formatted.
                *charactercomics_ids* (list) charactercomic ids that need to be created.
    - **get_character** gets a marvel character based on the name.
        - Parameters 
            *name*  (required, string): characters name.
            *character_model* (required, ModelBase): character model.
            *charactercomic_model* (required, ModelBase): charactercomic model.
        - Returns
                *result* (list) marvel character formatted
    - **get_and_store_comics_and_teammates** gets all the comics a character is in, based in the character id, and then iterates throught the comics, formats them, and gets all the characters (teammates) in it, formats them and stores characters, comics, creates relationship between them and updates the character that is passed as parameter.
        - Parameters 
            *character*  (object, string): character query from DB.
            *character_model* (required, ModelBase): character model.
            *charactercomic_model* (required, ModelBase): charactercomic model.
            *comic_model* (required, ModelBase): comic model.
            *serializer_comic* (required, SerializerMetaclass): comic serializer.
            *serializer_character* (required, SerializerMetaclass): character serializer.
            *serializer_charactercomic* (required, SerializerMetaclass): charactercomic serializer.
            *serializer_comic* (required, SerializerMetaclass): comic serializer.
        - Returns
                *count_teammates* (integer) teammates added to the DB.
                *count_comics* (integer) comics added to the DB.
- `views.py` has the endpoints that are explained in the **Endpoints** section bellow. 

## Run 
   On shell do `make up`
   
## Tests
  `make test`
   
## Endpoints

- **api/get-and-store-character**
    Gets the information, from marvel API, of a character based on the name and stores it on DB, if the character already exists on the DB returns the information of the DB.
    - *Parameter:*
        - name (required, string): name of the character
    - Example of return 
    ```
    {
        "info": [
            {
                "id": 1010705,
                "name": "Spectrum",
                "description": "",
                "imageURL": "http://i.annihil.us/u/prod/marvel/i/mg/9/00/4c0030bee8c86",
                "imageFullURL": "http://i.annihil.us/u/prod/marvel/i/mg/9/00/4c0030bee8c86.jpg",
                "imageExtension": "jpg"
            }
        ]
    }
    ```
 
- **api/get-and-store-comics-and-teammates**
    Get all the comics the character belongs to (the character must be already store on DB) and gets all the characters that are in those comics.
    - *Parameter:*
        - name (required, string): name of the character
    - Example of return
    ```
    {
        "info": [
            {
                "id": 101114,
                "title": "Thunderbolts (2022) #3",
                "description": null,
                "upc": "75960620386400311",
                "imageURL": "http://i.annihil.us/u/prod/marvel/i/mg/3/b0/6352e59c4148c",
                "imageFullURL": "http://i.annihil.us/u/prod/marvel/i/mg/3/b0/6352e59c4148c.jpg",
                "imageExtension": "jpg",
                "characters": [
                    {
                        "id": 1009338,
                        "name": "Hawkeye",
                        "description": "",
                        "imageURL": "http://i.annihil.us/u/prod/marvel/i/mg/e/90/50fecaf4f101b",
                        "imageFullURL": "http://i.annihil.us/u/prod/marvel/i/mg/e/90/50fecaf4f101b.jpg",
                        "imageExtension": "jpg",
                        "hasAllTeammates": false
                    },
                    {
                        "id": 1010360,
                        "name": "Thunderbolts",
                        "description": "After a battle with Onslaught left the world without the majority of the heroes that made it feel safe, Baron Zemo devised a plan like no other in order to rule the world. Zemo gathered Beetle, Fixer, Goliath, Moonstone, and Screaming Mimi, all former members of the Masters of Evil, together to disguise themselves as a new heroic team in order to take advantage of the missing heroes and gain the trust of the authorities and public in general.",
                        "imageURL": "http://i.annihil.us/u/prod/marvel/i/mg/b/a0/50fec50a26dc1",
                        "imageFullURL": "http://i.annihil.us/u/prod/marvel/i/mg/b/a0/50fec50a26dc1.jpg",
                        "imageExtension": "jpg",
                        "hasAllTeammates": false
                    },
                    {
                        "id": 1010705,
                        "name": "Spectrum",
                        "description": "",
                        "imageURL": "http://i.annihil.us/u/prod/marvel/i/mg/9/00/4c0030bee8c86",
                        "imageFullURL": "http://i.annihil.us/u/prod/marvel/i/mg/9/00/4c0030bee8c86.jpg",
                        "imageExtension": "jpg",
                        "hasAllTeammates": true
                    },
                    {
                        "id": 1017824,
                        "name": "Ms. America (America Chavez)",
                        "description": "",
                        "imageURL": "http://i.annihil.us/u/prod/marvel/i/mg/b/40/image_not_available",
                        "imageFullURL": "http://i.annihil.us/u/prod/marvel/i/mg/b/40/image_not_available.jpg",
                        "imageExtension": "jpg",
                        "hasAllTeammates": false
                    }
                ]
            },
            {
                "id": 101115,
                "title": "Thunderbolts (2022) #4",
                "description": null,
                "upc": "75960620386400411",
                "imageURL": "http://i.annihil.us/u/prod/marvel/i/mg/1/20/63725579dc239",
                "imageFullURL": "http://i.annihil.us/u/prod/marvel/i/mg/1/20/63725579dc239.jpg",
                "imageExtension": "jpg",
                "characters": [
                    {
                        "id": 1009338,
                        "name": "Hawkeye",
                        "description": "",
                        "imageURL": "http://i.annihil.us/u/prod/marvel/i/mg/e/90/50fecaf4f101b",
                        "imageFullURL": "http://i.annihil.us/u/prod/marvel/i/mg/e/90/50fecaf4f101b.jpg",
                        "imageExtension": "jpg",
                        "hasAllTeammates": false
                    },
                    {
                        "id": 1010360,
                        "name": "Thunderbolts",
                        "description": "After a battle with Onslaught left the world without the majority of the heroes that made it feel safe, Baron Zemo devised a plan like no other in order to rule the world. Zemo gathered Beetle, Fixer, Goliath, Moonstone, and Screaming Mimi, all former members of the Masters of Evil, together to disguise themselves as a new heroic team in order to take advantage of the missing heroes and gain the trust of the authorities and public in general.",
                        "imageURL": "http://i.annihil.us/u/prod/marvel/i/mg/b/a0/50fec50a26dc1",
                        "imageFullURL": "http://i.annihil.us/u/prod/marvel/i/mg/b/a0/50fec50a26dc1.jpg",
                        "imageExtension": "jpg",
                        "hasAllTeammates": false
                    },
                    {
                        "id": 1010705,
                        "name": "Spectrum",
                        "description": "",
                        "imageURL": "http://i.annihil.us/u/prod/marvel/i/mg/9/00/4c0030bee8c86",
                        "imageFullURL": "http://i.annihil.us/u/prod/marvel/i/mg/9/00/4c0030bee8c86.jpg",
                        "imageExtension": "jpg",
                        "hasAllTeammates": true
                    },
                    {
                        "id": 1017824,
                        "name": "Ms. America (America Chavez)",
                        "description": "",
                        "imageURL": "http://i.annihil.us/u/prod/marvel/i/mg/b/40/image_not_available",
                        "imageFullURL": "http://i.annihil.us/u/prod/marvel/i/mg/b/40/image_not_available.jpg",
                        "imageExtension": "jpg",
                        "hasAllTeammates": false
                    }
                ]
            }
        ],
        "added number teammates": 3,
        "added number comics": 2
    }
    ```
    
- **api/get-character**
    Get a character information from DB
    - *Parameter:*
        - name (required, string): name of the character
        
    - example of return
    ```
    {
        "info": [
            {
                "id": 1010705,
                "name": "Spectrum",
                "description": "",
                "imageURL": "http://i.annihil.us/u/prod/marvel/i/mg/9/00/4c0030bee8c86",
                "imageFullURL": "http://i.annihil.us/u/prod/marvel/i/mg/9/00/4c0030bee8c86.jpg",
                "imageExtension": "jpg",
                "hasAllTeammates": true,
                "created_at": "2023-03-09T18:44:18.964582Z",
                "updated_at": "2023-03-09T20:05:58.539937Z"
            }
        ]
    }
    ```
    - ***Note*** `hasAllTeammates` turns true when the comics and teammates of a character has been fetched from marvel API.
    
- **get-teammates**
    Get all the teammates a character has had.
    - *Parameter:*
        - name (required, string): name of the character
    - example of return
    ```
    {
        "total": 4,
        "characters": [
            {
                "id": 1009338,
                "name": "Hawkeye",
                "description": "",
                "imageURL": "http://i.annihil.us/u/prod/marvel/i/mg/e/90/50fecaf4f101b",
                "imageFullURL": "http://i.annihil.us/u/prod/marvel/i/mg/e/90/50fecaf4f101b.jpg",
                "imageExtension": "jpg",
                "hasAllTeammates": false,
                "created_at": "2023-03-09T18:25:22.738518Z",
                "updated_at": null
            },
            {
                "id": 1010360,
                "name": "Thunderbolts",
                "description": "After a battle with Onslaught left the world without the majority of the heroes that made it feel safe, Baron Zemo devised a plan like no other in order to rule the world. Zemo gathered Beetle, Fixer, Goliath, Moonstone, and Screaming Mimi, all former members of the Masters of Evil, together to disguise themselves as a new heroic team in order to take advantage of the missing heroes and gain the trust of the authorities and public in general.",
                "imageURL": "http://i.annihil.us/u/prod/marvel/i/mg/b/a0/50fec50a26dc1",
                "imageFullURL": "http://i.annihil.us/u/prod/marvel/i/mg/b/a0/50fec50a26dc1.jpg",
                "imageExtension": "jpg",
                "hasAllTeammates": false,
                "created_at": "2023-03-09T18:25:22.768072Z",
                "updated_at": null
            },
            {
                "id": 1010705,
                "name": "Spectrum",
                "description": "",
                "imageURL": "http://i.annihil.us/u/prod/marvel/i/mg/9/00/4c0030bee8c86",
                "imageFullURL": "http://i.annihil.us/u/prod/marvel/i/mg/9/00/4c0030bee8c86.jpg",
                "imageExtension": "jpg",
                "hasAllTeammates": true,
                "created_at": "2023-03-09T18:23:39.618016Z",
                "updated_at": "2023-03-09T18:25:23.278901Z"
            },
            {
                "id": 1017824,
                "name": "Ms. America (America Chavez)",
                "description": "",
                "imageURL": "http://i.annihil.us/u/prod/marvel/i/mg/b/40/image_not_available",
                "imageFullURL": "http://i.annihil.us/u/prod/marvel/i/mg/b/40/image_not_available.jpg",
                "imageExtension": "jpg",
                "hasAllTeammates": false,
                "created_at": "2023-03-09T18:25:22.753290Z",
                "updated_at": null
            }
        ]
    }
    ```
- **api/get-all-characters**
    Gets all the characters stored on DB.
    - example of return
    ```
    {
        "total": 4,
        "characters": [
            {
                "id": 1009338,
                "name": "Hawkeye",
                "description": "",
                "imageURL": "http://i.annihil.us/u/prod/marvel/i/mg/e/90/50fecaf4f101b",
                "imageFullURL": "http://i.annihil.us/u/prod/marvel/i/mg/e/90/50fecaf4f101b.jpg",
                "imageExtension": "jpg",
                "hasAllTeammates": false,
                "created_at": "2023-03-09T18:25:22.738518Z",
                "updated_at": null
            },
            {
                "id": 1010360,
                "name": "Thunderbolts",
                "description": "After a battle with Onslaught left the world without the majority of the heroes that made it feel safe, Baron Zemo devised a plan like no other in order to rule the world. Zemo gathered Beetle, Fixer, Goliath, Moonstone, and Screaming Mimi, all former members of the Masters of Evil, together to disguise themselves as a new heroic team in order to take advantage of the missing heroes and gain the trust of the authorities and public in general.",
                "imageURL": "http://i.annihil.us/u/prod/marvel/i/mg/b/a0/50fec50a26dc1",
                "imageFullURL": "http://i.annihil.us/u/prod/marvel/i/mg/b/a0/50fec50a26dc1.jpg",
                "imageExtension": "jpg",
                "hasAllTeammates": false,
                "created_at": "2023-03-09T18:25:22.768072Z",
                "updated_at": null
            },
            {
                "id": 1010705,
                "name": "Spectrum",
                "description": "",
                "imageURL": "http://i.annihil.us/u/prod/marvel/i/mg/9/00/4c0030bee8c86",
                "imageFullURL": "http://i.annihil.us/u/prod/marvel/i/mg/9/00/4c0030bee8c86.jpg",
                "imageExtension": "jpg",
                "hasAllTeammates": true,
                "created_at": "2023-03-09T18:23:39.618016Z",
                "updated_at": "2023-03-09T18:25:23.278901Z"
            },
            {
                "id": 1017824,
                "name": "Ms. America (America Chavez)",
                "description": "",
                "imageURL": "http://i.annihil.us/u/prod/marvel/i/mg/b/40/image_not_available",
                "imageFullURL": "http://i.annihil.us/u/prod/marvel/i/mg/b/40/image_not_available.jpg",
                "imageExtension": "jpg",
                "hasAllTeammates": false,
                "created_at": "2023-03-09T18:25:22.753290Z",
                "updated_at": null
            }
        ]
    }
    ```
- **api/get-all-comic**
    Gets all comics stored on DB
    - Returns 
    ```
    {
        "total": 2,
        "Comics": [
            {
                "id": 101114,
                "title": "Thunderbolts (2022) #3",
                "description": null,
                "upc": "75960620386400311",
                "imageURL": "http://i.annihil.us/u/prod/marvel/i/mg/3/b0/6352e59c4148c",
                "imageFullURL": "http://i.annihil.us/u/prod/marvel/i/mg/3/b0/6352e59c4148c.jpg",
                "imageExtension": "jpg",
                "created_at": "2023-03-08T22:20:26.807557Z",
                "updated_at": null
            },
            {
                "id": 101115,
                "title": "Thunderbolts (2022) #4",
                "description": null,
                "upc": "75960620386400411",
                "imageURL": "http://i.annihil.us/u/prod/marvel/i/mg/1/20/63725579dc239",
                "imageFullURL": "http://i.annihil.us/u/prod/marvel/i/mg/1/20/63725579dc239.jpg",
                "imageExtension": "jpg",
                "created_at": "2023-03-08T22:20:26.407604Z",
                "updated_at": null
            }
        ]
    }
    ```

## Improvements

- **Rate limiting**, regulate the number of request in a period of time by user. example by endpoint allow 3 request  with a difference of 0.5 sec but only 3 times under 5 secs but only 20 times under 60 secs.
- **Caching**, use a cache for the information most commonly queried for each endpoint, to keep the cache relevant use the strategy of keeping in the cache the most frequents used.
- **Availability**, using a cloud provider with 5 nines of availability in order to the solution be the most time only through the year (only around 5.5 mins of downtime through the year).
- **Logging and monitoring**, use an application such as datadog to do monitoring of what happens in the REST API, and get alerts in case something wrong is happening.
- **HTTPS**, run the solution over HTTPS to guarantee security.
- **Pagination** to add to the endpoints that return a lot of information (for example `/api/get-all-characters` and `/api/get-all-comics`) a `limit` and `offset` to return part of the result to the user.
- **DB** switch to a persistent storage such as PostgreSQL, so we can queries from the REST API that allows `.distinct(*fields)`