'''
https://www.wikidata.org/wiki/Wikidata:Pywikibot_-_Python_3_Tutorial/Data_Harvest

'''
import pywikibot
import pdb;
#
# site = pywikibot.Site("en", "wikipedia")
# page = pywikibot.Page(site, "Douglas Adams")
# item = pywikibot.ItemPage.fromPage(page)
#
# print(item)
#
#
# item_dict = item.get()
# print(item_dict.keys())
#
# import pdb;pdb.set_trace()


'''
# search for wiki ID:

# Connect to English Wikipedia
site = pywikibot.Site('en', 'wikipedia')

# Search for the page 'Lady Susan'
page = pywikibot.Page(site, 'Lady Susan')

# Get the item linked to this page
item = pywikibot.ItemPage.fromPage(page)

# Fetch the item details
item.get()

# Print the Wikidata ID
print("Wikidata ID:", item.id)

'''

import pywikibot

# Connect to Wikidata
site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()

# Get the item for "Lady Susan"
# Note: You need the correct Wikidata ID for "Lady Susan"
item = pywikibot.ItemPage(repo, "Q1497")  # Example: Q7364 is the ID for "Lady Susan"
item.get()

# Print all properties and their values (in ID)
# for property in item.claims:
#     print("Property:", property)
#     for claim in item.claims[property]:
#         claim_target = claim.getTarget()
#         pdb.set_trace()
#         print("\tValue:", claim_target)
# print names
for property in item.claims:
    print("Property:", property)
    for claim in item.claims[property]:
        claim_target = claim.getTarget()
        if isinstance(claim_target, pywikibot.ItemPage):
            # Fetch the label of the linked entity
            claim_target.get()
            print("\tEntity Name:", claim_target.labels.get('en', 'No label in English'))
        else:
            # For non-item targets (like dates, numbers), print their value
            print("\tValue:", claim_target)