<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>도서관 책찾기 - 즐겨찾기</title>
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', sans-serif;
    }

    body {
      background-color: #f5f5f7;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      padding: 20px;
    }

    /* 모바일 프레임 스타일 */
    .app-container {
      width: 100%;
      max-width: 380px;
      background-color: #ffffff;
      border: 1px solid #e0e0e0;
      border-radius: 16px;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }

    /* 상단 헤더 */
    .header {
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      padding: 16px;
      border-bottom: 1px solid #eee;
    }

    .back-btn {
      position: absolute;
      left: 16px;
      background: none;
      border: none;
      font-size: 20px;
      cursor: pointer;
      color: #333;
    }

    .header-title {
      font-size: 20px;
      font-weight: bold;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .heart-icon {
      color: #ff6b81;
    }

    /* 검색 바 영역 */
    .search-container {
      padding: 14px 16px;
      border-bottom: 1px solid #eee;
      display: flex;
      align-items: center;
      gap: 10px;
      background-color: #fafafa;
    }

    .search-icon {
      font-size: 20px;
    }

    .search-input {
      width: 100%;
      border: none;
      background: transparent;
      font-size: 16px;
      outline: none;
      color: #333;
    }

    .search-input::placeholder {
      color: #888;
    }

    /* 도서 리스트 영역 */
    .book-list {
      list-style: none;
      display: flex;
      flex-direction: column;
    }

    .book-item {
      display: flex;
      align-items: flex-start;
      padding: 20px 16px;
      border-bottom: 1px solid #eee;
      position: relative;
    }

    .book-item:last-child {
      border-bottom: none;
    }

    /* 책 아이콘 레벨 */
    .book-tag {
      width: 14px;
      height: 48px;
      border-radius: 3px;
      margin-right: 14px;
      flex-shrink: 0;
      margin-top: 2px;
    }

    .tag-red { background-color: #e57373; }
    .tag-green { background-color: #81c784; }
    .tag-blue { background-color: #64b5f6; }

    /* 책 정보 */
    .book-info {
      flex: 1;
      padding-right: 30px;
    }

    .book-title {
      font-size: 18px;
      font-weight: bold;
      color: #222;
      margin-bottom: 4px;
    }

    .book-author {
      font-size: 14px;
      color: #666;
      margin-bottom: 8px;
    }

    .book-location {
      font-size: 16px;
      font-weight: 600;
      color: #111;
    }

    /* 즐겨찾기 하트 버튼 */
    .fav-btn {
      position: absolute;
      right: 16px;
      top: 20px;
      background: none;
      border: none;
      font-size: 22px;
      cursor: pointer;
      color: #111;
    }

    .fav-btn.active {
      color: #ff4757;
    }

    /* 검색 결과 없을 때 */
    .no-result {
      padding: 40px;
      text-align: center;
      color: #888;
      font-size: 15px;
      display: none;
    }
  </style>
</head>
<body>

  <div class="app-container">
    <!-- 헤더 -->
    <header class="header">
      <button class="back-btn" onclick="alert('이전 페이지로 이동합니다.')">&lt;-</button>
      <h1 class="header-title">
        <span class="heart-icon">🩷</span>즐겨찾기
      </h1>
    </header>

    <!-- 검색창 -->
    <div class="search-container">
      <span class="search-icon">🔍</span>
      <input type="text" id="searchInput" class="search-input" placeholder="즐겨찾는 책 검색" onkeyup="filterBooks()">
    </div>

    <!-- 책 목록 -->
    <ul class="book-list" id="bookList">
      <!-- 책 1 -->
      <li class="book-item">
        <div class="book-tag tag-red"></div>
        <div class="book-info">
          <div class="book-title">아몬드</div>
          <div class="book-author">손원평</div>
          <div class="book-location">2층 문학 3번 서가</div>
        </div>
        <button class="fav-btn active" onclick="toggleFavorite(this)">♥</button>
      </li>

      <!-- 책 2 -->
      <li class="book-item">
        <div class="book-tag tag-green"></div>
        <div class="book-info">
          <div class="book-title">달러구트 꿈 백화점</div>
          <div class="book-author">이미예</div>
          <div class="book-location">2층 문학 5번 서가</div>
        </div>
        <button class="fav-btn active" onclick="toggleFavorite(this)">♥</button>
      </li>

      <!-- 책 3 -->
      <li class="book-item">
        <div class="book-tag tag-blue"></div>
        <div class="book-info">
          <div class="book-title">시관을 파는 상점</div>
          <div class="book-author">김선영</div>
          <div class="book-location">2층 문학 2번 서가</div>
        </div>
        <button class="fav-btn active" onclick="toggleFavorite(this)">♥</button>
      </li>
    </ul>

    <div id="noResult" class="no-result">검색 결과가 없습니다.</div>
  </div>

  <script>
    // 책 검색 기능
    function filterBooks() {
      const query = document.getElementById('searchInput').value.toLowerCase();
      const bookItems = document.querySelectorAll('.book-item');
      let visibleCount = 0;

      bookItems.forEach(item => {
        const title = item.querySelector('.book-title').textContent.toLowerCase();
        const author = item.querySelector('.book-author').textContent.toLowerCase();
        
        if (title.includes(query) || author.includes(query)) {
          item.style.display = 'flex';
          visibleCount++;
        } else {
          item.style.display = 'none';
        }
      });

      const noResult = document.getElementById('noResult');
      noResult.style.display = visibleCount === 0 ? 'block' : 'none';
    }

    // 즐겨찾기 토글 기능
    function toggleFavorite(btn) {
      if (btn.classList.contains('active')) {
        btn.classList.remove('active');
        btn.textContent = '♡';
      } else {
        btn.classList.add('active');
        btn.textContent = '♥';
      }
    }
  </script>
</body>
</html>
