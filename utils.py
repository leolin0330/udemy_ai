from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper
# import os

def generate_script(subject, video_length,creativity, api_key):
    title_template = ChatPromptTemplate.from_messages(
        [
            ("human", "請為'{subject}'這個主題的影片想一個吸引人的主題")
        ]
    )
    script_template = ChatPromptTemplate.from_messages(
        [
            ("human",
             """你是一位短視頻頻道的博主。根據以下標題和相關信息，為短視頻頻道寫一個視頻腳本。
             視頻標題：{title}，視頻時長：{duration}分鐘，生成的腳本的長度盡量遵循視頻時長的要求。
             要求開頭抓住限球，中間提供幹貨內容，結尾有驚喜，腳本格式也請按照【開頭、中間，結尾】分隔。
             整體內容的表達方式要盡量輕松有趣，吸引年輕人。
             腳本內容可以結合以下維基百科搜索出的信息，但僅作為參考，只結合相關的即可，對不相關的進行忽略：
             ```{wikipedia_search}```"""
             )
        ]
    )

    model = ChatOpenAI(openai_api_key = api_key, temperature = creativity)

    title_chain = title_template | model
    script_chain =script_template | model

    title = title_chain.invoke({"subject" : subject}).content

    search = WikipediaAPIWrapper(lang = "zh")
    search_result = search.run(subject)

    script = script_chain.invoke({"title": title, "duration": video_length,
                                  "wikipedia_search": search_result}).content

    return search_result, title, script

# print(generate_script("sora模型", 1, 0.7, os.getenv("OPENAI_API_KEY")))

