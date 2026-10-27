
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>도서 위치 검색</title>
    <!-- Tailwind CSS 로드 -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class', // 수동으로 다크모드 제어
        }
    </script>
    <!-- 아이콘 로드 -->
    <script src="https://unpkg.com/@phosphor-icons/web"></script>
    <style>
        /* Pretendard 웹폰트 적용 */
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
        body { font-family: 'Pretendard', sans-serif; }
        
        /* 사이드바 스크롤바 숨기기 (깔끔하게 보이기 위함) */
        .no-scrollbar::-webkit-scrollbar { display: none; }
        .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
    </style>
</head>
<body class="bg-slate-50 dark:bg-slate-900 transition-colors duration-300">
    
    <!-- 상단 네비게이션 바 -->
    <header class="bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700 p-4 flex justify-between items-center transition-colors duration-300">
        <div class="flex items-center gap-2 text-blue-500 dark:text-blue-400">
            <i class="ph ph-book-open text-3xl"></i>
            <h1 class="text-xl font-bold text-slate-800 dark:text-white">도서 위치 검색</h1>
        </div>
        <div class="flex items-center gap-5 text-slate-600 dark:text-slate-300">
            <!-- 다크모드 토글 버튼 -->
            <button id="theme-toggle" class="hover:text-blue-500 transition-colors flex items-center p-1 rounded-full bg-slate-100 dark:bg-slate-700">
                <i class="ph ph-moon text-xl" id="theme-icon"></i>
            </button>
            <a href="#" class="hover:text-blue-500 flex items-center gap-1"><i class="ph ph-house text-lg"></i> 홈</a>
            <a href="#" class="hover:text-blue-500 flex items-center gap-1"><i class="ph ph-magnifying-glass text-lg"></i> 검색</a>
            <a href="#" class="hover:text-blue-500 flex items-center gap-1"><i class="ph ph-user text-lg"></i> 로그인</a>
        </div>
    </header>

    <main class="max-w-7xl mx-auto p-4 md:p-8 flex flex-col lg:flex-row gap-8">
        
        <!-- 왼쪽 메인 영역 -->
        <div class="flex-1 flex flex-col gap-8">
            <!-- 중앙 검색 카드 -->
            <div class="bg-white dark:bg-slate-800 rounded-3xl p-10 flex flex-col items-center justify-center text-center shadow-sm border border-slate-100 dark:border-slate-700 transition-colors duration-300 py-24">
                <div class="text-blue-500 dark:text-blue-400 mb-6">
                    <i class="ph ph-book-open text-6xl"></i>
                </div>
                <h2 class="text-5xl font-extrabold text-slate-800 dark:text-white mb-4 tracking-tight">도서 위치 <span class="text-blue-500 dark:text-blue-400">검색</span></h2>
                <p class="text-xl text-slate-500 dark:text-slate-400 mb-10">원하는 책을 더 빠르고, 더 쉽게!</p>
                
                <!-- 검색창 -->
                <div class="w-full max-w-2xl relative flex items-center group">
                    <i class="ph ph-magnifying-glass absolute left-6 text-2xl text-slate-400 group-focus-within:text-blue-500 transition-colors"></i>
                    <input type="text" placeholder="찾고 싶은 책 제목을 입력해보세요!" class="w-full pl-16 pr-32 py-5 rounded-full border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 dark:text-white text-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 dark:focus:ring-blue-900 transition-all shadow-sm">
                    <button class="absolute right-2 bg-blue-500 hover:bg-blue-600 text-white rounded-full p-4 transition-colors">
                        <i class="ph ph-magnifying-glass text-xl"></i>
                    </button>
                </div>

                <!-- 해시태그 -->
                <div class="flex flex-wrap gap-3 mt-8 justify-center">
                    <span class="px-5 py-2.5 bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 rounded-full text-sm font-medium hover:bg-slate-200 dark:hover:bg-slate-600 cursor-pointer transition-colors"># 인기 도서</span>
                    <span class="px-5 py-2.5 bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 rounded-full text-sm font-medium hover:bg-slate-200 dark:hover:bg-slate-600 cursor-pointer transition-colors"># 신간 도서</span>
                    <span class="px-5 py-2.5 bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 rounded-full text-sm font-medium hover:bg-slate-200 dark:hover:bg-slate-600 cursor-pointer transition-colors"># 베스트셀러</span>
                    <span class="px-5 py-2.5 bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 rounded-full text-sm font-medium hover:bg-slate-200 dark:hover:bg-slate-600 cursor-pointer transition-colors"># 원하는 책 찾기</span>
                </div>
            </div>

            <!-- 하단 4가지 특징 카드 영역 -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="bg-white dark:bg-slate-800 p-8 rounded-3xl flex flex-col items-center text-center shadow-sm border border-slate-100 dark:border-slate-700 transition-colors duration-300 hover:-translate-y-1 transform transition-transform">
                    <div class="bg-blue-50 dark:bg-blue-900/40 p-4 rounded-full text-blue-500 dark:text-blue-400 mb-5">
                        <i class="ph ph-magnifying-glass text-3xl"></i>
                    </div>
                    <h3 class="font-bold text-slate-800 dark:text-white mb-2 text-lg">간편한 검색</h3>
                    <p class="text-sm text-slate-500 dark:text-slate-400 leading-relaxed">책 제목, 저자, 키워드로<br>쉽게 검색할 수 있어요.</p>
                </div>
                <div class="bg-white dark:bg-slate-800 p-8 rounded-3xl flex flex-col items-center text-center shadow-sm border border-slate-100 dark:border-slate-700 transition-colors duration-300 hover:-translate-y-1 transform transition-transform">
                    <div class="bg-blue-50 dark:bg-blue-900/40 p-4 rounded-full text-blue-500 dark:text-blue-400 mb-5">
                        <i class="ph ph-map-pin text-3xl"></i>
                    </div>
                    <h3 class="font-bold text-slate-800 dark:text-white mb-2 text-lg">도서 위치 확인</h3>
                    <p class="text-sm text-slate-500 dark:text-slate-400 leading-relaxed">찾고 있는 책의 정확한<br>위치를 알려드려요.</p>
                </div>
                <div class="bg-white dark:bg-slate-800 p-8 rounded-3xl flex flex-col items-center text-center shadow-sm border border-slate-100 dark:border-slate-700 transition-colors duration-300 hover:-translate-y-1 transform transition-transform">
                    <div class="bg-blue-50 dark:bg-blue-900/40 p-4 rounded-full text-blue-500 dark:text-blue-400 mb-5">
                        <i class="ph ph-book-open-text text-3xl"></i>
                    </div>
                    <h3 class="font-bold text-slate-800 dark:text-white mb-2 text-lg">신간 도서 확인</h3>
                    <p class="text-sm text-slate-500 dark:text-slate-400 leading-relaxed">지금 가장 인기 있는<br>새로운 책들을 만나보세요.</p>
                </div>
                <div class="bg-white dark:bg-slate-800 p-8 rounded-3xl flex flex-col items-center text-center shadow-sm border border-slate-100 dark:border-slate-700 transition-colors duration-300 hover:-translate-y-1 transform transition-transform">
                    <div class="bg-blue-50 dark:bg-blue-900/40 p-4 rounded-full text-blue-500 dark:text-blue-400 mb-5">
                        <i class="ph ph-lightning text-3xl"></i>
                    </div>
                    <h3 class="font-bold text-slate-800 dark:text-white mb-2 text-lg">빠르고 정확하게</h3>
                    <p class="text-sm text-slate-500 dark:text-slate-400 leading-relaxed">원하는 책을 더 빠르고,<br>더 쉽게 찾아보세요.</p>
                </div>
            </div>
        </div>

        <!-- 오른쪽 사이드바 (새로 들어온 책) -->
        <aside class="w-full lg:w-96 bg-white dark:bg-slate-800 rounded-3xl p-8 shadow-sm border border-slate-100 dark:border-slate-700 flex flex-col transition-colors duration-300 h-fit">
            <div class="flex items-center gap-2 text-blue-500 dark:text-blue-400 mb-8">
                <i class="ph-fill ph-sparkle text-2xl"></i>
                <h2 class="text-xl font-bold text-slate-800 dark:text-white">새로 들어온 책</h2>
            </div>
            
            <div class="flex-1 flex flex-col gap-6">
                <!-- 도서 아이템 1 -->
                <div class="flex gap-5 group cursor-pointer border-b border-slate-100 dark:border-slate-700 pb-6 last:border-0">
                    <div class="w-20 h-28 bg-[#8DB0C9] rounded-lg flex-shrink-0 shadow-md overflow-hidden relative border border-slate-200 dark:border-slate-600">
                        <div class="absolute inset-0 flex flex-col items-center justify-center p-2 text-center text-white">
                            <span class="text-xs font-bold drop-shadow-md">불편한<br>편의점</span>
                        </div>
                    </div>
                    <div class="flex-1 flex flex-col justify-center">
                        <h3 class="text-lg font-bold text-slate-800 dark:text-white group-hover:text-blue-500 transition-colors line-clamp-1">불편한 편의점</h3>
                        <p class="text-sm text-slate-500 dark:text-slate-400 mt-1">김호연</p>
                        <div class="mt-3">
                            <span class="px-3 py-1 bg-slate-100 dark:bg-slate-700 text-slate-500 dark:text-slate-300 text-xs rounded-full font-medium">소설</span>
                        </div>
                    </div>
                    <div class="flex items-center text-slate-300 dark:text-slate-500 group-hover:text-blue-500 transition-colors">
                        <i class="ph ph-caret-right text-2xl"></i>
                    </div>
                </div>

                <!-- 도서 아이템 2 -->
                <div class="flex gap-5 group cursor-pointer border-b border-slate-100 dark:border-slate-700 pb-6 last:border-0">
                    <div class="w-20 h-28 bg-[#0F224A] rounded-lg flex-shrink-0 shadow-md overflow-hidden relative border border-slate-200 dark:border-slate-600">
                        <div class="absolute inset-0 flex flex-col items-center justify-center p-2 text-center text-white">
                            <span class="text-xs font-bold drop-shadow-md">달러구트<br>꿈 백화점</span>
                        </div>
                    </div>
                    <div class="flex-1 flex flex-col justify-center">
                        <h3 class="text-lg font-bold text-slate-800 dark:text-white group-hover:text-blue-500 transition-colors line-clamp-1">달러구트 꿈 백화점</h3>
                        <p class="text-sm text-slate-500 dark:text-slate-400 mt-1">이미예</p>
                        <div class="mt-3">
                            <span class="px-3 py-1 bg-slate-100 dark:bg-slate-700 text-slate-500 dark:text-slate-300 text-xs rounded-full font-medium">소설</span>
                        </div>
                    </div>
                    <div class="flex items-center text-slate-300 dark:text-slate-500 group-hover:text-blue-500 transition-colors">
                        <i class="ph ph-caret-right text-2xl"></i>
                    </div>
                </div>
            </div>
        </aside>
    </main>

    <!-- 다크모드 자바스크립트 -->
    <script>
        const themeToggleBtn = document.getElementById('theme-toggle');
        const themeIcon = document.getElementById('theme-icon');
        
        themeToggleBtn.addEventListener('click', () => {
            // HTML 태그에 dark 클래스 토글
            document.documentElement.classList.toggle('dark');
            
            // 아이콘 변경 (달 <-> 해)
            if (document.documentElement.classList.contains('dark')) {
                themeIcon.classList.replace('ph-moon', 'ph-sun');
            } else {
                themeIcon.classList.replace('ph-sun', 'ph-moon');
            }
        });
    </script>
</body>
</html>
