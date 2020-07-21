import tweepy
import database


class TweetListener(tweepy.StreamListener):
    def __init__(self):
        super().__init__()
        self.db = database.init()
        print('init')

    def on_status(self, status, callback=1):
        if(str(status.text).startswith("RT") == False and "#covid19" in str(status.text)):
            try:
                doc_ref = self.db.collection('tweets').document(status.id_str)

                doc_ref.set({
                    'name': status.user.name,
                    'username': status.user.screen_name,
                    'text': status.text,
                    'profile_image': status.user.profile_image_url,
                    'approved': 0
                })

                print('salvo')
            except AttributeError:
                pass
