import streamlit as st
from vyzeai.agents.prebuilt_agents import ResearchAgent, VideoAudioBlogAgent, YTBlogAgent, BlogAgent, VideoAgent, EmailAgent

if 'api_key' not in st.session_state:
    st.session_state['api_key'] = None
if 'content' not in st.session_state:
    st.session_state['content'] = None
if 'image_path' not in st.session_state:
    st.session_state['image_path'] = None
if 'file_path' not in st.session_state:
    st.session_state['file_path'] = None

# st.write(st.session_state)
st.title("Blog Manager")

api_key = st.text_input("Enter opeani api key", type='password', key='api_key')
option = st.selectbox("Select one", ('website url to blog', 'youtube url to blog', 'video/audio to blog', 'website url to video'), placeholder="choose one", key='selectbox_option')
if option == 'website url to blog' or option == 'website url to video':
    topic = st.text_input("Enter the topic", key='topic')
    url = st.text_input("Enter a website url", key='url')
if option == 'youtube url to blog':
    yt_url = st.text_input("Enter a YouTube url", key='yt_url')
if option == 'video/audio to blog':
    file = st.file_uploader("Upload video or audio file", type=['mp4', 'mp3'], key='video/audio')
    # st.write(file)
    if file:
        with open(file.name, "wb") as f:
            f.write(file.getbuffer())
        st.session_state['file_path'] = file.name

if st.session_state.api_key:
    if st.button("submit"):
        if st.session_state['selectbox_option'] == 'website url to blog':
            research_agent = ResearchAgent(st.session_state.api_key)
            # linkedin_agent = LinkedInAgent(st.session_state.api_key)
            blog_agent = BlogAgent(api_key)

            context = research_agent.research(topic, url)

            contents = blog_agent.generate_blog(topic, url, context)
            st.write(contents[0][0])
            st.image(contents[-1][-1][0])
            st.session_state['content'] = contents[0][1]
            st.session_state['image_path'] = contents[-1][-1][0]
            
        if st.session_state['selectbox_option'] == 'youtube url to blog':
            # research_agent = ResearchAgent(st.session_state.api_key)
            yt_agent = YTBlogAgent(api_key)
            # linkedin_agent = LinkedInAgent(st.session_state.api_key)

            # context = research_agent.research(topic, url)
            # context = yt_agent.extract_transcript(st.session_state.yt_url)

            # content, image_path = linkedin_agent.generate_linkedin_post(context)
            contents = yt_agent.generate_blog(st.session_state.yt_url)
            st.write(contents[0][0])
            st.image(contents[-1][-1][0])
            st.session_state['content'] = contents[0][1]
            st.session_state['image_path'] = contents[-1][-1][0]

        if st.session_state['selectbox_option'] == 'video/audio to blog':
            # research_agent = ResearchAgent(st.session_state.api_key)
            va_agent = VideoAudioBlogAgent(api_key)
            # linkedin_agent = LinkedInAgent(st.session_state.api_key)

            # context = research_agent.research(topic, url)
            # st.write(st.session_state.file_path)
            contents = va_agent.generate_blog(st.session_state.file_path)

            st.write(contents[0][0])
            st.image(contents[-1][-1][0])
            st.session_state['content'] = contents[0][1]
            st.session_state['image_path'] = contents[-1][-1][0]

        if st.session_state['selectbox_option'] == 'website url to video':
            research_agent = ResearchAgent(st.session_state.api_key)
            video_agent = VideoAgent(api_key)

            context = research_agent.research(topic, url)
            content = video_agent.generate_video(topic, context)[0]
            st.video(content)
            st.session_state['content'] = content

    if st.session_state.content:
        to_mail = st.text_input("Enter your email address", key='to_mail')
        if st.button("send mail", key='mail_button'):
            email_agent = EmailAgent(api_key)
            ack = email_agent.send_email(to_mail, 'Your content', 'Thank you for using our product.', st.session_state.content, token_json_file_path='token.json')
            st.write(ack)

                



























# import streamlit as st
# from vyzeai.agents.prebuilt_agents import ResearchAgent, BlogAgent, EmailAgent

# def option_callback():
#     st.session_state['option'] = st.session_state['selectbox_option']
#     st.write(st.session_state.option)

# def email_callback():
#     # st.session_state['sender'] = st.se
#     st.write(st.session_state)
# if 'api_key' not in st.session_state:
#     st.session_state['api_key'] = None
# if 'blog' not in st.session_state:
#     st.session_state['blog'] = None

# st.write(st.session_state)
# st.title("Social Media Email Manager")

# api_key = st.text_input("Enter opeani api key", type='password', key='api_key')
# option = st.selectbox("select one", ('url_to_blog', 'url_to_video', 'yt_url_to_blog', 'video/audio_to_blog'), placeholder="choose one", on_change=option_callback, key='selectbox_option')
# topic = st.text_input("enter the topic", key='topic')
# url = st.text_input("enter the url", key='url')

# if st.session_state.api_key:
#     if st.button("submit"):
#         if st.session_state['selectbox_option'] == 'url_to_blog' and not st.session_state['blog']:
#             research_agent = ResearchAgent(st.session_state.api_key)
#             blog_agent = BlogAgent(st.session_state.api_key)

#             context = research_agent.research(topic, url)

#             blog = blog_agent.generate_blog(topic, url, context)
#             st.session_state['blog'] = blog

#     if st.session_state.blog:
#         to_mail = st.text_input("Enter receiver email address", key='to_mail')
#         subject = st.text_input("Enter email subject", key='subject')
#         body = st.text_input("Enter email body", key='body')
        
#         if st.button("send mail", on_click=email_callback, key='send_mail_button'):
#             email_agent = EmailAgent(api_key)
#             ack = email_agent.send_email(to_mail, subject, body)[0]
#             st.write(ack)

                



