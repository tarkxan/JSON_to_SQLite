#!/usr/bin/python3

'''
Created on Sep 3, 2018

@author: Lando
'''

#import apsw
import sqlite3
import glob
import json
import os.path

''' ------------------------------------------     
        querySqliteAndPrintResults
        
Insert data into a sqlite database and query it.       
------------------------------------------ '''
def querySqliteAndPrintResults(query, 
                               cursor,
                               res_header, 
                               title = "Running query:"):
    print()
    print(title)
    print(query)
    print(res_header)

    for record in cursor.execute(query):
        
        print(" " * 4, end = "")
        print("\t".join([str(f) for f in record]))
        
''' ------------------------------------------     
        querySqlite
        
Run necessary queries and print results        
------------------------------------------ '''
def querySqlite(cursor):
    
    # 0. Count the total number of images in the database
    query_0 = """
    SELECT COUNT(*) FROM image;
    """
    
    res_header = ' ' * 4 + 'NUMBER OF IMAGES\n' + ' ' * 4 + '-' * 16
    
    querySqliteAndPrintResults(query_0, 
                               cursor,
                               res_header, 
                               title = "Query 0")
    
    # 1. Count the total number of JSON documents in the database
    query_1 = '''
    select count(1) as num_of_JSON_files
    from   image i
    where  i.isDocument = 1
    ;
    '''
    
    res_header = ' ' * 4 + 'NUMBER OF JSON FILES\n' + ' ' * 4 + '-' * 20
    
    querySqliteAndPrintResults(query_1, 
                               cursor, 
                               res_header, 
                               title = "Query 1")

    # 2. Count the total number of Images, Labels, Landmarks,
    # Locations, Logos, Pages, and WebEntity:s in the database.
    query_2 = '''
    select 'number of images:\t\t\t' as item,
           count(1) as number
    from   image
    union all
    select 'number of labels:\t\t\t',
           count(1) as num_of_labels
    from   label       
    union all
    -- dictict mid, landmark descriptions counted
    -- if the same landmark description has different mid - it is counted twice
    select 'number of landmarks:\t\t',
           count(1) 
    from   (select distinct mid, description
            from   landmark)
    union all
    -- counts unique set of values for the fields longitude, latitude 
    select 'number of unique latitude, longitude:',
           count(1) as num_of_unique_latit_longit
    from   (select 1
            from   landmark
            group by longitude, latitude)
    union all
    select 'number of pages:\t\t\t',
           count(1) as num_of_pages
    from   page
    union all
    select 'number of entities:\t\t\t',
           count(1) as num_of_entities
    from   webentity
    ;
    '''
    
    res_header = ' ' * 4 + 'TITLE' + '\t' * 5 + 'QUANTITY\n' + ' ' * 4 + '-' * 52
    
    querySqliteAndPrintResults(query_2, 
                               cursor, 
                               res_header, 
                               title = "Query 2")

    # 3. List all of the Images that are associated with the
    # Label with an id of "/m/015kr" (which has the description
    # "bridge") ordered alphabetically by URL
    query_3 = '''
    select l.mid as label_mid,
           i.id  as image_id,
           i.url as image_url
    from   label              l,
           image_tagged_label itl,
           image              i
    where  l.mid = '/m/015kr'
      --and l.description = 'bridge'
      and  l.mid = itl.mid
      and  itl.imageId = i.id
    order by image_url
    ;
    '''
    
    res_header = ' ' * 3 + 'LABEL MID   IMAGE ID\t\tIMAGE URL\t\n' + '   ' + '-' * 85
    
    querySqliteAndPrintResults(query_3, 
                               cursor, 
                               res_header, 
                               title = "Query 3")

    # 4. List the 10 most frequent WebEntitys that are applied
    # to the same Images as the Label with an id of "/m/015kr" (which
    # has the description "bridge"). Order them by the number of times
    # they appear followed by their entityId alphabetically
    query_4 = '''
    select count(1)      as number_of_entities,
           w.entityId,
           w.description as entity
    from   label                  l,
           image_tagged_label     itl,
           image                  i,
           image_tagged_webEntity itw,
           webEntity              w
    where  l.mid        = '/m/015kr'
      and  l.mid        = itl.mid
      and  itl.imageId  = i.id
      and  i.id         = itw.imageId
      and  itw.entityId = w.entityId
    group by w.entityId, 
             w.description
    order by 1 desc,
             2 asc
    limit 10
    ;
    '''
    
    res_header = '  ENTITIES ENTITY ID\tENTITY DESCRIPTION\n' + ' ' * 2 + '-' * 40
    
    querySqliteAndPrintResults(query_4, 
                               cursor, 
                               res_header, 
                               title = "Query 4")

    # 5. Find Images associated with Landmarks that are not
    # "New York" (id "/m/059rby") or "New York City" (id "/m/02nd_")
    # ordered by image URL alphabetically
    query_5 = '''
    select i.id          as image_id,
           i.url         as image_url,
           l.description as landmark
    from   landmark                l,
           image_contains_landmark icl,
           image                   i
    where  l.mid         not in('/m/059rby', '/m/02nd_') 
      --and  l.description not in('New York', 'New York City')
      and  l.landmarkId  = icl.landmarkId
      and  icl.imageId   = i.id
    order by i.url asc
    ;
    '''
    
    res_header = ' ' * 3 + 'IMG ID' + '\t' * 3 + 'IMAGE URL' + '\t' * 4 + 'LANDMARK DESCRIPTION\n   ' + '-' * 100
    
    querySqliteAndPrintResults(query_5, 
                               cursor, 
                               res_header, 
                               title = "Query 5")

    # 6. List the 10 Labels that have been applied to the most
    # Images along with the number of Images each has been applied to
    query_6 = ''' 
    select l.mid,
           l.description  as label,
           count(1)       as num_of_images
    from   label               l,
           image_tagged_label  itl,
           image               i
    where  l.mid       = itl.mid
      and  itl.imageId = i.id
    group by l.mid, 
             l.description
    order by 3 desc
    limit 10
    ;
    '''
    
    res_header = '   LABEL_MID  LABEL_DESCRIPTION  IMAGES_QTY\n   ' + '-' * 40
    
    querySqliteAndPrintResults(query_6, 
                               cursor, 
                               res_header, 
                               title = "Query 6")

    # 7. List the 50 Images that are linked to the most Pages
    # through the webEntities.pagesWithMatchingImages JSON property
    # along with the number of Pages linked to each one.
    query_7 = '''
    select i.id              as image_id,
           i.url             as image_url,
           count(iip.pageId) as number_of_pages
    from   image          i,
           image_in_page  iip,
           page           p
    where  i.id        = iip.imageId
      and  iip.pageId  = p.pageId
    group by i.id
    order by number_of_pages desc,
             i.id asc
    limit 50
    ;
    '''
    
    res_header = '  IMG ID' + '\t' * 3 + 'PAGE URL' + '\t' * 4 + 'PAGES QTY\n  ' + '-' * 80
    
    querySqliteAndPrintResults(query_7, 
                               cursor, 
                               res_header, 
                               title = "Query 7")

    # 8. List the 10 pairs of Images that appear on the most
    # Pages together through the webEntities.pagesWithMatchingImages
    # JSON property. Order them by the number of pages that they
    # appear on together, then by the URL of the first. Make sure that
    # each pair is only listed once regardless of which is first and
    # which is second.
    query_8 = """
    select count(i.id),
           p.pageId,
           p.url,
           pair_p.pageId,
           pair_p.url
    from   page            p,
           image_in_page   iip,
           image           i,
           image_in_page   pair_iip,
           page            pair_p       
    where  p.pageId        = iip.pageId
      and  iip.imageId     = i.id
      and  i.isDocument    = 1
      and  iip.imageId     = pair_iip.imageId
      and  pair_iip.pageId = pair_p.pageId 
      and  pair_p.pageId   > p.pageId
    group by p.pageId,
             p.url,
             pair_p.pageId,
             pair_p.url
    order by count(i.id) desc,
             p.url asc
    limit 10         
    ;
    """
    
    res_header = '  TIMES PAGE ID' + '\t' * 2 + 'PAGE URL' + '\t' * 3 + 'PAGE ID' + '\t' * 3 + 'PAGE URL\n  ' + '-' * 140
    
    querySqliteAndPrintResults(query_8, 
                               cursor, 
                               res_header, 
                               title = "Query 8")
'''    
def updateImageIsDocument(cursor, 
                          table, 
                          whereDict):
    
    whereClauses = [f'`{k}` = :{k}' for k in whereDict]
    #select = f'select {keyName} from {table} where {" and ".join(whereClauses)}'
    
    #print(f'Updating {table}.isDocument for {table}.id = {imageId}\n')
    
    updateSmnt = f'update {table} set isDocument = 1 where {" and ".join(whereClauses)}'
    #print(updateSmnt)
    
    cursor.execute(updateSmnt, whereDict)
'''        
''' ------------------------------------------     
        getOrCreateRow
        
Return the ID of a row of the given table with the given data.
If the row does not already exists then create it first.  Existence is
determined by matching on all supplied values.  Table is name of table,
dataDict is a dict of {'attribute': value} pairs.     
------------------------------------------ '''
def getOrCreateRow(cursor, 
                   table, 
                   dataDict,
                   whereDict,
                   keyName):
    
    # create a query and run it
    whereClauses = [f'`{k}` = :{k}' for k in whereDict]
    select = f'select {keyName} from {table} where {" and ".join(whereClauses)}'
    #print(select)

    cursor.execute(select, 
                   dataDict)
    
    res = cursor.fetchone()
    
    # if a tuple exists - return its rownum
    if res is not None:
        return res[0]

    # concatenate fields / values for insert clause
    fields = ', '.join(f'`{field}`' for field in dataDict)
    values = ', '.join(f':{value}' for value in dataDict)
    insert = f'insert into {table} ({fields}) values({values})'
    #print(insert)
    
    # execute insert clause
    cursor.execute(insert,
                   dataDict)
    
    # fetch data after insert
    cursor.execute(select,
                   dataDict)
    
    res = cursor.fetchone()
    
    if res is not None:
        return res[0]
    
    raise Exception("Something went wrong with " + str(dataDict))        

''' ------------------------------------------     
        insertFileData       
------------------------------------------ '''   
def insertFileData(cursor, 
                   jsonData,
                   fileName):
    
    # 1. process image
    # 2. update isDocument attribute of image
    try:
        url = jsonData['url']
        dataDict = {'url': url, 'isDocument': 1}
        whereDict = {'url': url}
        
        imageId = getOrCreateRow(cursor, 
                                 'image',   # table name
                                 dataDict,  # data
                                 whereDict, # whereDict
                                 'id')      # keyName
        
        print(f'\tfile\'s {url} imageId: {imageId}')
        
    except KeyError:
        print('\t*******\n\tWARNING: Check the field URL in JSON file\n\t*******')
    

    # 2. update isDocument attribute of image
    # is populated during insert in the previous statement
    '''updateImageIsDocument(cursor,
                          'image',  # table name
                          dataDict)'''
    
    # 3. process labelAnnotations field
    try:
        for label in jsonData['response']['labelAnnotations']:
            
            dataDict = {'mid': label['mid'], 'description': label['description']}
            whereDict = {'mid': label['mid']}
            #print(dataDict)
            
            getOrCreateRow(cursor, 
                           'label',   # table name
                           dataDict,  # data
                           whereDict, 
                           'mid')     # key name
            
            # process image_tagged_label
            dataDict = {'imageId': imageId, 'mid': label['mid'], 'score': label['score']}
            whereDict = {'imageId': imageId, 'mid': label['mid']}
            #print(dataDict)
            
            getOrCreateRow(cursor, 
                           'image_tagged_label', # table name
                           dataDict,             # data
                           whereDict, 
                           'mid')                # key name
            
    except KeyError:
        print('\t*******\n\tWARNING: Check labelAnnotations fields in JSON file\n\t*******')

    # 4. process webDetection.fullMatchingImages field
    try:
        for image in jsonData['response']['webDetection']['fullMatchingImages']:
            
            dataDict = {'url': image['url'], 'isDocument': 0}
            whereDict = {'url': image['url']}
            
            #print(dataDict)
            
            matchedImageId = getOrCreateRow(cursor, 
                                            'image',   # table name
                                            dataDict,  # data
                                            whereDict,  # whereDict
                                            'id')      # keyName
            
            # process webDetection.fullMatchingImages
            dataDict = {'imageId': imageId, 'matchedImageId': matchedImageId, 'type': 'full'}
            whereDict = {'imageId': imageId, 'matchedImageId': matchedImageId}
            #print(dataDict)
            
            getOrCreateRow(cursor, 
                           'image_matches_image',   # table name
                           dataDict,                # data
                           whereDict,               # whereDict
                           'imageId')               # keyName
            
    except KeyError:
        print('\t*******\n\tWARNING: Check fields fullMatchingImages in JSON file\n\t*******')
    
    # 5. process webDetection.partialMatchingImages field
    try:
        for image in jsonData['response']['webDetection']['partialMatchingImages']:
            
            dataDict = {'url': image['url'], 'isDocument': 0}
            whereDict = {'url': image['url']}
            #print(dataDict)
                
            partMatchedImageId = getOrCreateRow(cursor, 
                                                'image',   # table name
                                                dataDict,  # data
                                                whereDict,  # whereDict
                                                'id')      # keyName
            
            # process webDetection.partialMatchingImages
            dataDict = {'imageId': imageId, 'matchedImageId': partMatchedImageId, 'type': 'partial'}
            whereDict = {'imageId': imageId, 'matchedImageId': partMatchedImageId}
            #print(dataDict)
            
            getOrCreateRow(cursor, 
                           'image_matches_image',   # table name
                           dataDict,                # data
                           whereDict,               # whereDict
                           'imageId')               # keyName
            
    except KeyError:
        print('\t*******\n\tWARNING: Check fields partialMatchingImages in JSON file\n\t*******')
    
    # 6. process webDetection.pagesWithMatchingImages field
    try:
        for page in jsonData['response']['webDetection']['pagesWithMatchingImages']:
            
            dataDict = {'url': page['url']}
            #print(dataDict)
            
            pageId = getOrCreateRow(cursor, 
                                    'page',    # table name
                                    dataDict,  # data
                                    dataDict, 
                                    'pageId')  # key name
            
            # populate table image_in_page
            dataDict = {'imageId': imageId, 'pageId': pageId}
            #print(dataDict)
            
            getOrCreateRow(cursor, 
                           'image_in_page',  # table name
                           dataDict,         # data
                           dataDict, 
                           'pageId')         # key name
            
    except KeyError:
        print('\t*******\n\tWARNING: Check fields pagesWithMatchingImages in JSON file\n\t*******')
            
    # 7. process webDetection.webEntities field
    try:
        for webEntity in jsonData['response']['webDetection']['webEntities']:
            
            try:
                entityDesc = webEntity['description']
                
            except:
                entityDesc = webEntity['entityId']
                print(f'\t*******\n\tWARNING:  file {fileName} - Web Entities description is null\n\t*******')
                 
            dataDict = {'entityId': webEntity['entityId'], 'description': entityDesc}
            whereDict = {'entityId': webEntity['entityId']}
            #print(dataDict)
            
            webEntityId = getOrCreateRow(cursor, 
                                         'webEntity',   # table name
                                         dataDict,      # data
                                         dataDict, 
                                         'entityId')    # key name
            
            # populate table image_tagged_webEntity
            dataDict = {'imageId': imageId, 'entityId': webEntityId, 'score': webEntity['score']}
            whereDict = {'imageId': imageId, 'entityId': webEntityId}
            
            getOrCreateRow(cursor,
                           'image_tagged_webEntity',  # table name
                           dataDict,                  # data      
                           whereDict,                             
                           'entityId')                # key name
            
    except KeyError:
        print('\t*******\n\tWARNING: Check fields webDetection.webEntities in JSON file\n\t*******') 

    
    # 8. process landmarkAnnotations field
    # 9. process landmarkAnnotations.locations field
    try:
        
        for landmark in jsonData['response']['landmarkAnnotations']:
            
            #print(landmark)
            
            try:
                description = landmark['description']
            except:
                description = landmark['mid']
                print(f'\t*******\n\tWARNING:  file {fileName} - landmark description is null\n\t*******')
            
            latitude = landmark.get('locations')[0]['latLng'].get('latitude')
            longitude = landmark.get('locations')[0]['latLng'].get('longitude')
            
            dataDict = {'mid': landmark['mid'], 'description': description, 'score': landmark['score'], 'longitude': longitude, 'latitude': latitude}
            #print(dataDict)
             
            landmarkId = getOrCreateRow(cursor, 
                                        'landmark',   # table name
                                        dataDict,     # data
                                        dataDict, 
                                        'landmarkId') # key name
            
            # process image_tagged_label
            dataDict = {'imageId': imageId, 'landmarkId': landmarkId}
            #print(dataDict)
            
            getOrCreateRow(cursor, 
                           'image_contains_landmark', # table name
                           dataDict,                  # data
                           dataDict,
                           'landmarkId')             # key name
            
    except KeyError:
        print('\t*******\n\tWARNING: Check fields landmarkAnnotations in JSON file\n\t*******')
        print('\t*******\n\tWARNING: Check fields landmarkAnnotations.locations in JSON file\n\t*******')  
            
    
''' ------------------------------------------     
    populateSqlite
    
Load the JSON results from google into sqlite. Assumes schema already created      
------------------------------------------ '''        
def populateSqlite(jsonDir, 
                   cursor):
    
    loaded = 0
    
    json_pattern = os.path.join(jsonDir, '*.json')
    fileList = glob.glob(json_pattern)  
    
    # for every file from the list populate tables
    for jsonFile in fileList:
        
        fileName = jsonFile[jsonFile.rindex('\\'[-1]) + 1:]
        print(f'\nLoading file {fileName} into SQLite Database')
        
        with open(jsonFile) as jf:
            
            jsonData = json.load(jf)
            #print('jSonData: ', jsonData)
            
            insertFileData(cursor, 
                           jsonData,
                           fileName)
            loaded += 1

    cursor.execute('commit;')

    print("\n\tLoaded", loaded, "JSON documents into Sqlite database\n")        

''' ------------------------------------------     
        createSchema
        
Create necessary tables in the sqlite database        
------------------------------------------ '''
def createSchema(cursor,
                 clearDb = True):
    
    # tables' names
    image = 'image'
    label = 'label'
    page = 'page'
    landmark = 'landmark'
    location = 'location'
    webEntity = 'webEntity'
    image_tagged_label = 'image_tagged_label'
    image_in_page= 'image_in_page'
    image_matches_image = 'image_matches_image'
    image_contains_landmark = 'image_contains_landmark'
    image_tagged_webEntity = 'image_tagged_webEntity'
    landmark_located_at_location = 'landmark_located_at_location'
    
    dropTblStmnt = 'drop table if exists '

    # drop schema tables
    if clearDb:
        cursor.execute(dropTblStmnt + image + ';')
        cursor.execute(dropTblStmnt + label + ';')
        cursor.execute(dropTblStmnt + page + ';')
        cursor.execute(dropTblStmnt + landmark + ';')
        cursor.execute(dropTblStmnt + location + ';')
        cursor.execute(dropTblStmnt + webEntity + ';')
        cursor.execute(dropTblStmnt + image_tagged_label + ';')
        cursor.execute(dropTblStmnt + image_in_page + ';')
        cursor.execute(dropTblStmnt + image_matches_image + ';')
        cursor.execute(dropTblStmnt + image_contains_landmark + ';')
        cursor.execute(dropTblStmnt + image_tagged_webEntity + ';')
        cursor.execute(dropTblStmnt + landmark_located_at_location + ';')
    
    # create schema tables
    cursor.execute('create table ' + image + '(id         integer      not null primary key, ' + 
                                              'url        varchar(256) not null, ' +
                                              'isDocument int(1));')

    cursor.execute('create table ' + label + '(mid         varchar(20) not null primary key, ' +
                                              'description varchr(256));')

    cursor.execute('create table ' + page + '(pageId integer      not null primary key, ' +
                                             'url    varchar(256) not null);')

    cursor.execute('create table ' + landmark + '(landmarkId  integer      not null primary key, ' +
                                                 'mid         varchar(20)  not null, ' +
                                                 'description varchar(256) not null, ' +
                                                 'score       real         not null, ' +
                                                 'longitude   real         not null, ' +
                                                 'latitude    real         not null);')

    cursor.execute('create table ' + webEntity + '(entityId     varchar(20)  not null primary key, ' +
                                                  'description  varchar(256));')

    cursor.execute('create table ' + image_tagged_label + '(imageId int(5) not null, ' +
                                                           'mid     int(5) not null, ' +
                                                           'score   real, ' +
                                                           'primary key(imageId, mid), ' +
                                                           'foreign key(imageId) references image(id), ' +
                                                           'foreign key(mid)     references label(mid));')

    cursor.execute('create table ' + image_in_page + '(imageId int(5) not null, ' +
                                                      'pageId  int(5) not null, ' +
                                                      'primary key(imageId, pageId), ' +
                                                      'foreign key(imageId) references image(id), ' +
                                                      'foreign key(pageId)  references page(pageId));')

    cursor.execute('create table ' + image_matches_image + '(imageId         int(5)      not null, ' +
                                                            'matchedImageId  int(5)      not null, ' +
                                                            'type            varchar(7)  not null, ' +
                                                            'check (type in(\'full\', \'partial\')), ' + 
                                                            'primary key(imageId, matchedImageId), ' +
                                                            'foreign key(imageId)        references image(id), ' +
                                                            'foreign key(matchedImageId) references image(id));')

    cursor.execute('create table ' + image_contains_landmark + '(imageId     int(5)      not null, ' +
                                                                'landmarkId  int(5)      not null, ' +
                                                                'primary key(imageId, landmarkId), ' +
                                                                'foreign key(imageId)     references image(id), ' +
                                                                'foreign key(landmarkId) references landmark(landmarkId));')

    cursor.execute('create table ' + image_tagged_webEntity + '(imageId  int(5)      not null, ' +
                                                               'entityId varchar(20) not null, ' +
                                                               'score    real, ' +
                                                               'primary key(imageId, entityId), ' +
                                                               'foreign key(imageId)  references image(id), ' +
                                                               'foreign key(entityId) references webEntity(entityId));')

    
''' ---------------------     
            main  
--------------------- '''
def main():
    
    dataDir = "data/"
	jsonDir = 'E:\\ProjectFiles\\json\\'
    dbFileName = 'sqlite.db'
    dbFile = os.path.join(jsonDir, dbFileName)
    
    connection = sqlite3.connect(dbFile)
    # create a cursor object
    cursor = connection.cursor()
    
    # create schema tables
    createSchema(cursor)
    
    # populate schema tables
    populateSqlite(jsonDir, 
                   cursor)
    
    # fetch data from schema tables
    querySqlite(cursor)
    connection.close()

if __name__ == '__main__':
    main()
