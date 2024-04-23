import os

class SaveToFilePipeline:
    def open_spider(self, spider):
        # Ensure the directory exists
        os.makedirs('documents', exist_ok=True)

    def process_item(self, item, spider):
        # Construct a filename from the item's 'id'
        filename = f"document_{item['id']}.txt"
        path = os.path.join('documents', filename)

        # Write the item's 'content' to a file
        with open(path, 'w', encoding='utf-8') as file:
            file.write(item['content'])
        return item
