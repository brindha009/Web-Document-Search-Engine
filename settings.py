# my_project/settings.py

BOT_NAME = 'my_project'

SPIDER_MODULES = ['my_project.spiders']
NEWSPIDER_MODULE = 'my_project.spiders'

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'my_project.pipelines.SaveToFilePipeline': 300,
}
