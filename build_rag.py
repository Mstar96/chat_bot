import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

#1.加载文档:遍历docs/下所有的txt文件,用TextLoader加载
docs = []
docs_dir = "docs"
for filename in os.listdir(docs_dir):
    if filename.endswith(".txt"):
        loader = TextLoader(os.path.join(docs_dir, filename),encoding="utf-8")
        docs.extend(loader.load())

#2.文本切分,用RecursiveCharacterTextSplitter切分文本,设置chunk_size=300,chunk_overlap=50
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 300,
    chunk_overlap = 50,
)
chunks = text_splitter.split_documents(docs)
print(f"切分后文本块数量: {len(chunks)}")

#3.embeddings初始化
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh")

#4.存储到chroma
vectorstore = Chroma.from_documents(
    documents = chunks,
    embedding = embeddings,
    persist_directory = "./chroma_db"
)
vectorstore.persist()
print("知识库构建完成")
