The project interacts with a set of JSON documents in SQLite. 
The JSON documents are the output of the Google Cloud Vision API applied 
to images returned from a Flickr API query for interesting images related
to the text "New York".


The annotations come from the Google Cloud Vision API and are described in
here https://cloud.google.com/vision/docs/reference/rest/v1/images/annotate#AnnotateImageResponse .
I have only included the following subset of those annotations, however:

`'landmarkAnnotations' -- identify geographical landmarks in photographs. 
For the purposes of discussing entities in the database
schema, this will add 'Landmarks', each of which can have zero or more 'Locations'
 
 'labelAnnotations' -- predict descriptive labels for images. This will
   add 'Label' entities to the schema.
   
'webDetection' -- predict the presence of web entities (things with
   names) in images along with pages that contain the image and other
   images that are similar. This will add 'WebEntity', 'Page', and 'Image'
   entities to the schema.
   
## Introduction to code   

All of the python code is contained in the file ['project.py'] and has

	 * DB schema creation
	 * DB population from JSON files
	 * DB queries



## Database tables

The meaning of most of the fields should be fairly clear, but there are two that need some explanation:
 
 'isDocument' in the 'image' table: This should be 1 if an image is the subject of an analysis 
    in the JSON file and 0 if an image only appears in the 'webDetection' fields
 
 'type' in the 'image_matches_image' table: This should be either "full" if it appears in 
   'webDetection.fullMatchingImages' and "partial" if it appears in 'webDetection.partialMatchingImages'

## DB population from JSON files
'insertImage()' is called with the JSON from the analysis of a single image by Google Cloud Vision API.
The 'json' module imports it so that JSON dictionaries become python dictionaries, and JSON lists become python lists.

## DB queries

	 1. Count the total number of JSON documents in the database
	 2. Count the total number of Images, Labels, Landmarks,
	    Locations, Logos, Pages, and WebEntity:s in the database.
	 3. List all of the Images that are associated with the
	    Label with an id of "/m/015kr" (which has the description
	    "bridge") ordered alphabetically by URL
	 4. List the 10 most frequent WebEntitys that are applied
	    to the same Images as the Label with an id of "/m/015kr" (which
	    has the description "bridge"). Order them by the number of times
	    they appear followed by their entityId alphabetically
	 5. Find Images associated with Landmarks that are not
	    "New York" (id "/m/059rby") or "New York City" (id "/m/02nd_")
	    ordered by image URL alphabetically.
	 6. List the 10 Labels that have been applied to the most
	    Images along with the number of Images each has been applied to
	 7. List the 50 Images that are linked to the most Pages
	    through the webEntities.pagesWithMatchingImages JSON property
	    along with the number of Pages linked to each one.
	 8. List the 10 pairs of Images that appear on the most
	    Pages together through the webEntities.pagesWithMatchingImages
	    JSON property. Order them by the number of pages that they
	    appear on together, then by the URL of the first. Make sure that
	    each pair is only listed once regardless of which is first and
	    which is second.
    
	
	
	1. Instructions for how to run the code to populate the database and to query the database:

		2.1. In Main function change variables values dbDir, jsonDir with path to a database and JSON files, respectively
		For instance:
		dbDir = 'E:\\Assignment1\\ProjectFiles\\databases'
		jsonDir = 'E:\\Assignment1\\ProjectFiles\\json\\'

		2.2. Run file project.py from any Python IDE / Interpreter


	2. The results from each of the queries:

		Query 0: Count the total number of images in the database

	----------------
	NUMBER OF IMAGES
	----------------
	560

	Query 1: Count the total number of JSON documents in the database

	--------------------
	NUMBER OF JSON FILES
	--------------------
	100

	Query 2: Count the total number of Images, Labels, Landmarks, Locations, Pages, and WebEntities in the database

	--------------------------------------------
	TITLE				QUANTITY
	--------------------------------------------
	number of images:			560
	number of labels:			201
	number of landmarks:		        18
	number of unique latitude, longitude:   26
	number of pages:			556
	number of entities:			451

	Query 3: List all of the Images that are associated with the Label with an id of "/m/015kr" (which has the description "bridge") ordered alphabetically by URL

    -------------------------------------------------------------------------------------
    LABEL MID   IMAGE ID	IMAGE URL	
    -------------------------------------------------------------------------------------
    /m/015kr	209	https://farm1.staticflickr.com/590/33188022342_1eeb39857f.jpg
    /m/015kr	161	https://farm3.staticflickr.com/2850/32712158102_ecc8f2cec3.jpg
    /m/015kr	459	https://farm4.staticflickr.com/3394/5828289828_9f9bb8a45a.jpg
    /m/015kr	1	https://farm4.staticflickr.com/3667/12640493983_c82eb338c3.jpg
    /m/015kr	195	https://farm4.staticflickr.com/3725/33062489846_e6c505493d.jpg
    /m/015kr	296	https://farm5.staticflickr.com/4238/34310239173_43c51169db.jpg
    /m/015kr	319	https://farm5.staticflickr.com/4254/34994427273_cac7762f17.jpg
    /m/015kr	325	https://farm5.staticflickr.com/4282/35024953080_c130ef296c.jpg
    /m/015kr	98	https://farm8.staticflickr.com/7585/17156902591_cebb2df72c.jpg
    /m/015kr	58	https://farm9.staticflickr.com/8574/15926352399_3ff75a6c31.jpg
    /m/015kr	81	https://farm9.staticflickr.com/8618/16654352517_49b28d1dfc.jpg

	Query 4: List the 10 most frequent WebEntitys that are applied to the same Images as the Label with an id of "/m/015kr" (which has the description "bridge"). Order them by the number of times they appear followed by their entityId alphabetically

	------------------------------------------ 
	ENTITIES ENTITY ID	ENTITY DESCRIPTION
	------------------------------------------
	7	/m/015kr	Bridge
	7	/m/051gs3	Bridge–tunnel
	7	/m/068jd	Photograph
	7	/m/0cv4c	Brooklyn Bridge
	5	/m/0204fg	Skyline
	5	/m/0cr3d	Brooklyn
	4	/m/04dtx9	Flickr
	4	/m/0csy8	Suspension bridge
	3	/g/1tk640vm	Brooklyn Bridge
	2	/g/11c7s__wzx	Things To Do In New York

	Query 5: Find Images associated with Landmarks that are not "New York" (id "/m/059rby") or "New York City" (id "/m/02nd_") ordered by image URL alphabetically

	--------------------------------------------------------------------------------------------
	IMAGE ID	IMAGE URL						LANDMARK DESCRIPTION
	--------------------------------------------------------------------------------------------
	209	https://farm1.staticflickr.com/590/33188022342_1eeb39857f.jpg	Brooklyn Bridge
	150	https://farm1.staticflickr.com/749/32192134004_1c0357ac04.jpg	125th Street Business Improvement District
	150	https://farm1.staticflickr.com/749/32192134004_1c0357ac04.jpg	Tom Otterness Studio
	440	https://farm2.staticflickr.com/1406/5116761560_e7fb406da1.jpg	New York City
	161	https://farm3.staticflickr.com/2850/32712158102_ecc8f2cec3.jpg	Brooklyn Bridge
	459	https://farm4.staticflickr.com/3394/5828289828_9f9bb8a45a.jpg	Manhattan Bridge
	195	https://farm4.staticflickr.com/3725/33062489846_e6c505493d.jpg	Brooklyn Bridge
	447	https://farm5.staticflickr.com/4081/5443157673_9854560f3b.jpg	Statue of Liberty
	296	https://farm5.staticflickr.com/4238/34310239173_43c51169db.jpg	Brooklyn Bridge
	315	https://farm5.staticflickr.com/4241/34950973243_d6603ebaeb.jpg	Park Avenue
	319	https://farm5.staticflickr.com/4254/34994427273_cac7762f17.jpg	Williamsburg Bridge
	319	https://farm5.staticflickr.com/4254/34994427273_cac7762f17.jpg	Williamsburg Bridge
	408	https://farm5.staticflickr.com/4343/36557009266_462534ebae.jpg	MetLife Building
	422	https://farm5.staticflickr.com/4433/36877559755_1ac1e22d0b.jpg	Statue of Liberty
	477	https://farm6.staticflickr.com/5234/5837391149_5423460f3a.jpg	New York City
	134	https://farm8.staticflickr.com/7206/26903887842_295193cb2f.jpg	Seattle Public Library
	134	https://farm8.staticflickr.com/7206/26903887842_295193cb2f.jpg	One World Financial Center
	12	https://farm8.staticflickr.com/7365/14158959691_de873f0610.jpg	Flatiron Building
	12	https://farm8.staticflickr.com/7365/14158959691_de873f0610.jpg	Flatiron Building
	38	https://farm8.staticflickr.com/7546/15687461383_7dc37cb572.jpg	Times Square
	81	https://farm9.staticflickr.com/8618/16654352517_49b28d1dfc.jpg	Brooklyn Bridge


	Query 6: List the 10 Labels that have been applied to the most Images along with the number of Images each has been applied to
 
	---------------------------------------------------
	LABEL MID	LABEL DESCRIPTION	IMAGES QTY

	--------------------------------------------------
	/m/056mk	metropolis		55
	/m/01n32	city			52
	/m/039jbq	urban area		51
	/m/0j_s4	metropolitan area	50
	/m/05_5t0l	landmark		48
	/m/01bqvp	sky	                47
	/m/079cl	skyscraper		44
	/m/034z7h	cityscape		36
	/m/0204fg	skyline			34
	/m/0cgh4	building		32

	Query 7: List the 50 Images that are linked to the most Pages through the webEntities.pagesWithMatchingImages JSON property along with the number of Pages linked to each one

	---------------------------------------------------------------------------------
	IMAGE ID	PAGE URL						PAGES QTY
	------------------------------------------------------------------------------------
	17	https://farm4.staticflickr.com/3890/14818589943_5f207ea855.jpg	10
	38	https://farm8.staticflickr.com/7546/15687461383_7dc37cb572.jpg	10
	67	https://farm9.staticflickr.com/8657/16406546840_2f521a85e9.jpg	10
	81	https://farm9.staticflickr.com/8618/16654352517_49b28d1dfc.jpg	10
	98	https://farm8.staticflickr.com/7585/17156902591_cebb2df72c.jpg	10
	110	https://farm3.staticflickr.com/2361/2408044761_7d69296561.jpg	10
	137	https://farm8.staticflickr.com/7452/28091103345_140bcf6c55.jpg	10
	154	https://farm1.staticflickr.com/592/32679655584_86d7e7708c.jpg	10
	161	https://farm3.staticflickr.com/2850/32712158102_ecc8f2cec3.jpg	10
	174	https://farm3.staticflickr.com/2150/32746542692_fdf6fb9e5c.jpg	10
	191	https://farm3.staticflickr.com/2915/32849383944_ffed704408.jpg	10
	195	https://farm4.staticflickr.com/3725/33062489846_e6c505493d.jpg	10
	211	https://farm3.staticflickr.com/2896/33224081040_5b77fa38a1.jpg	10
	222	https://farm3.staticflickr.com/2863/33370959340_4d459be754.jpg	10
	234	https://farm4.staticflickr.com/3767/33385238882_e9d559c988.jpg	10
	246	https://farm4.staticflickr.com/3894/33549282836_05ce749a83.jpg	10
	258	https://farm3.staticflickr.com/2826/33559074896_0a7e662a57.jpg	10
	273	https://farm3.staticflickr.com/2930/34154725246_7c6f1c44e0.jpg	10
	307	https://farm5.staticflickr.com/4017/34914350744_804fe265a8.jpg	10
	319	https://farm5.staticflickr.com/4254/34994427273_cac7762f17.jpg	10
	352	https://farm5.staticflickr.com/4380/35519610183_382ae4203e.jpg	10
	359	https://farm5.staticflickr.com/4026/35613794445_9d873ce33a.jpg	10
	365	https://farm5.staticflickr.com/4300/35830140732_e8c9028f8a.jpg	10
	379	https://farm5.staticflickr.com/4323/36132615765_06e731e01e.jpg	10
	390	https://farm5.staticflickr.com/4434/36328882514_fde90bb7a3.jpg	10
	397	https://farm5.staticflickr.com/4351/36343385791_b0088fd51a.jpg	10
	404	https://farm5.staticflickr.com/4295/36344754535_0304f5a57a.jpg	10
	408	https://farm5.staticflickr.com/4343/36557009266_462534ebae.jpg	10
	413	https://farm5.staticflickr.com/4368/36629020652_496ea18d4d.jpg	10
	422	https://farm5.staticflickr.com/4433/36877559755_1ac1e22d0b.jpg	10
	432	https://farm5.staticflickr.com/4091/5092088834_6dd783676f.jpg	10
	447	https://farm5.staticflickr.com/4081/5443157673_9854560f3b.jpg	10
	455	https://farm4.staticflickr.com/3518/5762413992_d4a3d7a976.jpg	10
	459	https://farm4.staticflickr.com/3394/5828289828_9f9bb8a45a.jpg	10
	467	https://farm4.staticflickr.com/3048/5833292987_009b5bc1c2.jpg	10
	499	https://farm9.staticflickr.com/8179/7998458383_fa27b624b6.jpg	10
	516	https://farm9.staticflickr.com/8356/8255650216_da89c3a0fc.jpg	10
	531	https://farm9.staticflickr.com/8394/8746286862_3cb9181a32.jpg	10
	540	https://farm6.staticflickr.com/5474/9108473536_596ceff041.jpg	10
	5	https://farm3.staticflickr.com/2901/14134372024_f7cae3649a.jpg	9
	271	https://farm3.staticflickr.com/2881/33753757991_ef6800477d.jpg	9
	299	https://farm5.staticflickr.com/4167/34534047521_7b95f7483e.jpg	9
	315	https://farm5.staticflickr.com/4241/34950973243_d6603ebaeb.jpg	9
	332	https://farm5.staticflickr.com/4207/35327027566_8e3e20da95.jpg	9
	375	https://farm5.staticflickr.com/4310/36103547802_db8069f85e.jpg	9
	384	https://farm5.staticflickr.com/4297/36179455866_aaa00f94dd.jpg	9
	440	https://farm2.staticflickr.com/1406/5116761560_e7fb406da1.jpg	9
	485	https://farm6.staticflickr.com/5313/5888487773_1ae966751e.jpg	9
	12	https://farm8.staticflickr.com/7365/14158959691_de873f0610.jpg	8
	60	https://farm8.staticflickr.com/7572/16082905372_20e0f80b1f.jpg	8

	Query 8: List the 10 pairs of Images that appear on the most Pages together through the webEntities.pagesWithMatchingImages JSON property. 
	Order them by the number of pages that they appear on together, then by the URL of the first. 
	Make sure that each pair is only listed once regardless of which is first and which is second

	--------------------------------------------------------------------------------------------   
	TIMES PAGE ID		PAGE URL				PAGE ID             PAGE URL
	--------------------------------------------------------------------------------------------
	5	154	https://www.flickr.com/photos/tags/tintography/		323	https://picssr.com/tags/wideangel
	4	141	http://freephotostags.com/new%20york			142	http://freephotostags.com/home/new+champion+5+glosm%C3%A4staren
	4	254	https://nabewise.com/nyc/bronx-river/			259	https://nabewise.com/nyc/city-island/
	3	142	http://freephotostags.com/home/new+champion+5+glosm%C3%A4staren  143	 http://www.keywordsfr.com/bmV3IGF0JmFtcDt0IHBob25lcw/
	3	 141	http://freephotostags.com/new%20york			143	http://www.keywordsfr.com/bmV3IGF0JmFtcDt0IHBob25lcw/
	3	 258	http://photopin.com/free-photos/new-york-city		260	http://photopin.com/free-photos/nyc-marathon/2
	3	 455	http://www.flickriver.com/photos/danielmennerich/sets/72157625323790968/ 456	https://www.flickr.com/photos/danielmennerich/page48/
	3	 255	https://hiveminer.com/Tags/helicopter%2Cny		259	https://nabewise.com/nyc/city-island/
	3	 256	https://hiveminer.com/Tags/new,ny			259	https://nabewise.com/nyc/city-island/
	3	 254	https://nabewise.com/nyc/bronx-river/			255	https://hiveminer.com/Tags/helicopter%2Cny