Well I understand the cookies. Now I need to understand the routing and working of these urls: \
@core_apps/users/urls.py How do the paths in this file tie to the paths in @config/urls.py and how do they tie to the paths in djoser and 
SOCIAL_AUTH_ALLOWED_REDIRECT_URIS and we also have this env variable 
REDIRECT_URIS="http://localhost:8080/api/v1/auth/google,http://localhost/api/v1/auth/complete/google-oauth2/"  how do the @core_apps/users/serializers.py fit in the 
picture?\
I need a good explanation of routing in django not necessarily how cookies are added to the request and response cycle. 







great can you make anki cards for these files @core_apps/profiles/pipeline.py, @core_apps/profiles/serializers.py, @.core_apps/common/renderers.py
@ core_apps/profiles/urls.py, @core_apps/profiles/tasks.py, @core_apps/profiles/views.py
When thinking of the questions bear in mind that I use anki for a long period thus the question  must make sense independently Secondly the answer should not be long. Structure questions well so that the answers are less than 50 words if possible less than 20 words.