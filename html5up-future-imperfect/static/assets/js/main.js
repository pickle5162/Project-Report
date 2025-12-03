function createNewPost(data) {
    const {
        title, 
        subtitle, 
        link, 
        date, 
        dateDisplay, 
        authorName, 
        authorAvatarSrc, 
        featuredImageSrc, 
        excerpt, 
        category, 
        likes, 
        comments
    } = data; 
    
    const mainContainer = document.getElementById("main");
    if (!mainContainer) {
        console.error("找不到 ID 為 'main' 的容器！");
        return;
    }

    // 1. 創建 <article class="post">
    const article = document.createElement("article");
    article.classList.add("post");

    // 2. 創建 <header>
    const header = document.createElement("header");

    // 2a. 創建標題區塊 <div class="title">
    const titleDiv = document.createElement("div");
    titleDiv.classList.add("title");

    const h2 = document.createElement("h2");
    const h2Link = document.createElement("a");
    h2Link.href = link;
    h2Link.textContent = title;
    h2.appendChild(h2Link);
    
    const pSubtitle = document.createElement("p");
    pSubtitle.textContent = subtitle;

    titleDiv.appendChild(h2);
    titleDiv.appendChild(pSubtitle);
    
    // 2b. 創建資訊區塊 <div class="meta">
    const metaDiv = document.createElement("div");
    metaDiv.classList.add("meta");

    const time = document.createElement("time");
    time.classList.add("published");
    time.setAttribute("datetime", date);
    time.textContent = dateDisplay;

    const authorLink = document.createElement("a");
    authorLink.href = "#";
    authorLink.classList.add("author");
    
    const authorNameSpan = document.createElement("span");
    authorNameSpan.classList.add("name");
    authorNameSpan.textContent = authorName;
    
    const authorImg = document.createElement("img");
    authorImg.src = authorAvatarSrc;
    authorImg.alt = authorName;
    

    authorLink.appendChild(authorNameSpan);
    authorLink.appendChild(authorImg);

    metaDiv.appendChild(time);
    metaDiv.appendChild(authorLink);

    header.appendChild(titleDiv);
    header.appendChild(metaDiv);

    // 3. 創建圖片連結 <a class="image featured">
    const imageLink = document.createElement("a");
    imageLink.href = link;
    imageLink.classList.add("image", "featured");
    
    const image = document.createElement("img");
    image.src = featuredImageSrc;
    image.alt = title;
    imageLink.appendChild(image);

    // 4. 創建摘要段落 <p>
    const excerptParagraph = document.createElement("p");
    excerptParagraph.textContent = excerpt;

    // 5. 創建 <footer>
    const footer = document.createElement("footer");

    // 5a. 動作按鈕 <ul class="actions">
    const actionsUl = document.createElement("ul");
    actionsUl.classList.add("actions");
    const actionsLi = document.createElement("li");
    const actionsLink = document.createElement("a");
    actionsLink.href = link;
    actionsLink.classList.add("button", "large");
    actionsLink.textContent = "Continue Reading";
    actionsLi.appendChild(actionsLink);
    actionsUl.appendChild(actionsLi);

    // 5b. 統計數據 <ul class="stats">
    const statsUl = document.createElement("ul");
    statsUl.classList.add("stats");

    // Category
    statsUl.innerHTML += `<li><a href="#">${category}</a></li>`;
    // Likes
    statsUl.innerHTML += `<li><a href="#" class="icon solid fa-heart">${likes}</a></li>`;
    // Comments
    statsUl.innerHTML += `<li><a href="#" class="icon solid fa-comment">${comments}</a></li>`;

    footer.appendChild(actionsUl);
    footer.appendChild(statsUl);

    // 6. 將所有部分組合到 <article> 中
    article.appendChild(header);
    article.appendChild(imageLink);
    article.appendChild(excerptParagraph);
    article.appendChild(footer);

    // 7. 將新的文章添加到主容器 (mainContainer)
    mainContainer.appendChild(article);
}


// =========================================================
// 事件處理邏輯 (Event Handling Logic)
// =========================================================

// 1. 取得按鈕元素
const addButton = document.getElementById("addPostButton");

// 2. 基礎的文章資料模板
const samplePostData = {
    title: "基礎模板", 
    subtitle: "這是透過按鈕點擊動態生成的文章。",
    link: "#",
    date: new Date().toISOString().slice(0, 10), 
    dateDisplay: new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' }),
    authorName: "動態產生者",
    authorAvatarSrc: "images/avatar.jpg", 
    featuredImageSrc: "images/pic05.jpg", // 每次都用一個不同的圖片路徑
    excerpt: "這個區塊的內容是透過 JavaScript 程式碼創建出來的...",
    category: "Dynamic",
    likes: 0,
    comments: 0
};

// 3. 處理點擊事件的函數
function handleAddPostClick() {
    // 每次點擊時，創建一個新的物件，並更新獨特的內容
    const newPostData = {
        ...samplePostData, // 複製基礎數據
        title: "最新文章 - " + new Date().toLocaleTimeString('zh-TW', {hour12: false}), // 標題包含時間
        likes: Math.floor(Math.random() * 100) + 1, // 隨機讚數
        comments: Math.floor(Math.random() * 50) + 1, // 隨機評論數
        date: new Date().toISOString().slice(0, 10),
        dateDisplay: new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
    };

    // 呼叫文章創建函數
    createNewPost(newPostData);
}

// 4. 監聽點擊事件
if (addButton) {
    addButton.addEventListener('click', handleAddPostClick);
} else {
    console.error("找不到 ID 為 'addPostButton' 的按鈕！請檢查您的 HTML。");
}
















