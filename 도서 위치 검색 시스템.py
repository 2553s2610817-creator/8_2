<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>도서 위치 검색</title>
    
    <!-- Pretendard Font -->
    <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable.min.css" />
    
    <!-- Phosphor Icons -->
    <script src="https://unpkg.com/@phosphor-icons/web"></script>
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['"Pretendard Variable"', 'Pretendard', '-apple-system', 'BlinkMacSystemFont', 'system-ui', 'Roboto', 'sans-serif'],
                    },
                    colors: {
                        primary: {
                            DEFAULT: '#4A89FF',
                            50: '#F0F5FF',
                            100: '#E0EBFF',
                            600: '#2A69FF',
                        },
                        surface: '#F8FAFC',
                    }
                }
            }
        }
    </script>
    <style>
        body {
            background-color: #ffffff;
            color: #1E293B;
        }
        
        /* Book Cover Gradients */
        .cover-1 { background: linear-gradient(135deg, #A7C7E7 0%, #7DA0C4 100%); }
        .cover-2 { background: linear-gradient(135deg, #1A365D 0%, #2C5282 100%); }
        .cover-3 { background: linear-gradient(135deg, #FDE68A 0%, #FCD34D 100%); }
        .cover-4 { background: linear-gradient(135deg, #6EE7B7 0%, #3B82F6 100%); }

        /* Custom soft shadows */
        .shadow-soft {
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03), 0 1px 3px rgba(0, 0, 0, 0.02);
        }
        .shadow-inner-soft {
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.02);
        }
    </style>
</head>
<body class="min-h-screen antialiased flex flex-col selection:bg-primary selection:text-white">

    <!-- Header -->
    <header class="border-b border-gray-100 bg-white sticky top-0 z-10">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <!-- Logo -->
            <div class="flex items-center gap-2 cursor-pointer hover:opacity-80 transition-opacity">
                <i class="ph ph-book-open text-primary text-3xl"></i>
                <span class="text-xl font-bold tracking-tight">도서 위치 검색</span>
            </div>
            
            <!-- Navigation -->
            <nav class="flex items-center gap-6 text-sm font-medium text-gray-500">
                <a href="#" class="flex items-center gap-1.5 text-primary hover:text-primary-600 transition-colors">
                    <i class="ph ph-house text-lg"></i>
                    홈
                </a>
                <a href="#" class="flex items-center gap-1.5 hover:text-gray-900 transition-colors">
                    <i class="ph ph-magnifying-glass text-lg"></i>
                    검색
                </a>
                <a href="#" class="flex items-center gap-1.5 hover:text-gray-900 transition-colors">
                    <i class="ph ph-user text-lg"></i>
                    로그인
                </a>
            </nav>
        </div>
    </header>

    <!-- Main Content -->
    <main class="flex-grow">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 lg:py-16">
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-10">
                
                <!-- Left Column: Main Search Area (70%) -->
                <div class="lg:col-span-8 flex flex-col items-center pt-8">
                    
                    <!-- Hero Section -->
                    <div class="text-center mb-10 w-full">
                        <!-- Hero Illustration -->
                        <div class="flex justify-center mb-6 relative">
                            <div class="relative text-primary">
                                <i class="ph ph-book-open-text text-7xl"></i>
                                <!-- Decorative sparks -->
                                <i class="ph-fill ph-sparkle absolute -top-2 -left-6 text-primary/40 text-xl"></i>
                                <i class="ph-fill ph-sparkle absolute -bottom-2 -right-8 text-primary/40 text-2xl"></i>
                                <i class="ph-fill ph-sparkle absolute top-2 -right-4 text-primary/30 text-sm"></i>
                            </div>
                        </div>
                        
                        <h1 class="text-4xl sm:text-5xl md:text-6xl font-extrabold text-gray-800 tracking-tight mb-4">
                            도서 위치 <span class="text-primary">검색</span>
                        </h1>
                        <p class="text-lg text-gray-500 font-medium">원하는 책을 더 빠르고, 더 쉽게!</p>
                    </div>

                    <!-- Search Bar -->
                    <div class="w-full max-w-3xl relative mb-6">
                        <div class="relative flex items-center w-full h-16 sm:h-20 rounded-full bg-white border border-gray-200 shadow-soft overflow-hidden pl-6 pr-2 sm:pr-3 focus-within:border-primary focus-within:ring-4 focus-within:ring-primary-50 transition-all duration-300">
                            <i class="ph ph-magnifying-glass text-gray-400 text-2xl mr-3"></i>
                            <input 
                                type="text" 
                                placeholder="찾고 싶은 책 제목을 입력해보세요!" 
                                class="w-full h-full outline-none text-lg text-gray-700 bg-transparent placeholder-gray-400"
                            >
                            <button class="flex items-center justify-center bg-primary hover:bg-primary-600 text-white rounded-full w-12 h-12 sm:w-14 sm:h-14 flex-shrink-0 transition-colors shadow-md">
                                <i class="ph ph-magnifying-glass text-xl sm:text-2xl font-bold"></i>
                            </button>
                        </div>
                    </div>

                    <!-- Tags -->
                    <div class="flex flex-wrap justify-center gap-3 mb-16 max-w-2xl">
                        <button class="px-5 py-2 rounded-full bg-primary-50 text-gray-600 text-sm font-medium hover:bg-primary-100 hover:text-primary transition-colors"># 인기 도서</button>
                        <button class="px-5 py-2 rounded-full bg-primary-50 text-gray-600 text-sm font-medium hover:bg-primary-100 hover:text-primary transition-colors"># 신간 도서</button>
                        <button class="px-5 py-2 rounded-full bg-primary-50 text-gray-600 text-sm font-medium hover:bg-primary-100 hover:text-primary transition-colors"># 베스트셀러</button>
                        <button class="px-5 py-2 rounded-full bg-primary-50 text-gray-600 text-sm font-medium hover:bg-primary-100 hover:text-primary transition-colors"># 원하는 책 찾기</button>
                    </div>

                    <!-- Features Bottom Section -->
                    <div class="w-full bg-surface rounded-3xl p-6 sm:p-8 md:p-10">
                        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 divide-y sm:divide-y-0 sm:divide-x divide-gray-200">
                            <!-- Feature 1 -->
                            <div class="flex flex-col items-center text-center px-4 pt-4 sm:pt-0">
                                <div class="w-14 h-14 rounded-full bg-primary-50 text-primary flex items-center justify-center mb-4">
                                    <i class="ph ph-magnifying-glass text-2xl"></i>
                                </div>
                                <h3 class="font-bold text-gray-800 mb-2">간편한 검색</h3>
                                <p class="text-sm text-gray-500 leading-relaxed">책 제목, 저자, 키워드로<br>쉽게 검색할 수 있어요.</p>
                            </div>
                            <!-- Feature 2 -->
                            <div class="flex flex-col items-center text-center px-4 pt-4 sm:pt-0">
                                <div class="w-14 h-14 rounded-full bg-primary-50 text-primary flex items-center justify-center mb-4">
                                    <i class="ph ph-map-pin text-2xl"></i>
                                </div>
                                <h3 class="font-bold text-gray-800 mb-2">도서 위치 확인</h3>
                                <p class="text-sm text-gray-500 leading-relaxed">찾고 있는 책의 정확한<br>위치를 알려드려요.</p>
                            </div>
                            <!-- Feature 3 -->
                            <div class="flex flex-col items-center text-center px-4 pt-4 sm:pt-0">
                                <div class="w-14 h-14 rounded-full bg-primary-50 text-primary flex items-center justify-center mb-4">
                                    <i class="ph ph-book-open text-2xl"></i>
                                </div>
                                <h3 class="font-bold text-gray-800 mb-2">신간 도서 확인</h3>
                                <p class="text-sm text-gray-500 leading-relaxed">지금 가장 인기 있는<br>새로운 책들을 만나보세요.</p>
                            </div>
                            <!-- Feature 4 -->
                            <div class="flex flex-col items-center text-center px-4 pt-4 sm:pt-0">
                                <div class="w-14 h-14 rounded-full bg-primary-50 text-primary flex items-center justify-center mb-4">
                                    <i class="ph ph-lightning text-2xl"></i>
                                </div>
                                <h3 class="font-bold text-gray-800 mb-2">빠르고 정확하게</h3>
                                <p class="text-sm text-gray-500 leading-relaxed">원하는 책을 더 빠르고,<br>더 쉽게 찾아보세요.</p>
                            </div>
                        </div>
                    </div>
                    
                </div>

                <!-- Right Column: Sidebar (30%) -->
                <div class="lg:col-span-4 mt-10 lg:mt-0">
                    <div class="bg-white rounded-3xl border border-gray-100 shadow-soft p-6 md:p-8 h-full">
                        
                        <!-- Sidebar Title -->
                        <div class="flex items-center gap-2 mb-6">
                            <i class="ph-fill ph-sparkle text-primary text-xl"></i>
                            <h2 class="text-xl font-bold text-gray-800">새로 들어온 책</h2>
                        </div>
                        
                        <!-- Book List -->
                        <div class="flex flex-col">
                            <!-- Book Item 1 -->
                            <a href="#" class="group flex items-center py-5 border-b border-gray-50 last:border-0 hover:bg-gray-50 -mx-4 px-4 transition-colors rounded-xl">
                                <div class="w-14 h-20 rounded-md shadow-sm overflow-hidden flex-shrink-0 cover-1 flex items-center justify-center relative">
                                     <div class="absolute inset-0 bg-white/20"></div>
                                     <i class="ph-fill ph-book text-white/50 text-2xl relative z-10"></i>
                                </div>
                                <div class="ml-4 flex-grow">
                                    <h3 class="font-bold text-gray-800 text-[15px] mb-1 group-hover:text-primary transition-colors">불편한 편의점</h3>
                                    <p class="text-sm text-gray-400 mb-2">김호연</p>
                                    <span class="inline-block px-2.5 py-1 bg-primary-50 text-primary-600 text-xs font-semibold rounded-full">소설</span>
                                </div>
                                <i class="ph ph-caret-right text-gray-300 text-xl group-hover:text-primary transition-colors ml-2"></i>
                            </a>

                            <!-- Book Item 2 -->
                            <a href="#" class="group flex items-center py-5 border-b border-gray-50 last:border-0 hover:bg-gray-50 -mx-4 px-4 transition-colors rounded-xl">
                                <div class="w-14 h-20 rounded-md shadow-sm overflow-hidden flex-shrink-0 cover-2 flex items-center justify-center relative">
                                     <div class="absolute inset-0 bg-black/10"></div>
                                     <i class="ph-fill ph-book text-white/50 text-2xl relative z-10"></i>
                                </div>
                                <div class="ml-4 flex-grow">
                                    <h3 class="font-bold text-gray-800 text-[15px] mb-1 group-hover:text-primary transition-colors">달러구트 꿈 백화점</h3>
                                    <p class="text-sm text-gray-400 mb-2">이미예</p>
                                    <span class="inline-block px-2.5 py-1 bg-primary-50 text-primary-600 text-xs font-semibold rounded-full">소설</span>
                                </div>
                                <i class="ph ph-caret-right text-gray-300 text-xl group-hover:text-primary transition-colors ml-2"></i>
                            </a>

                            <!-- Book Item 3 -->
                            <a href="#" class="group flex items-center py-5 border-b border-gray-50 last:border-0 hover:bg-gray-50 -mx-4 px-4 transition-colors rounded-xl">
                                <div class="w-14 h-20 rounded-md shadow-sm overflow-hidden flex-shrink-0 cover-3 flex items-center justify-center relative">
                                     <i class="ph-fill ph-book text-black/20 text-2xl relative z-10"></i>
                                </div>
                                <div class="ml-4 flex-grow">
                                    <h3 class="font-bold text-gray-800 text-[15px] leading-tight mb-1 group-hover:text-primary transition-colors">오늘 밤, 세계에서<br>이 사랑이 사라진다 해도</h3>
                                    <p class="text-sm text-gray-400 mb-2">이치조 미사키</p>
                                    <span class="inline-block px-2.5 py-1 bg-primary-50 text-primary-600 text-xs font-semibold rounded-full">소설</span>
                                </div>
                                <i class="ph ph-caret-right text-gray-300 text-xl group-hover:text-primary transition-colors ml-2"></i>
                            </a>

                            <!-- Book Item 4 -->
                            <a href="#" class="group flex items-center py-5 border-b border-gray-50 last:border-0 hover:bg-gray-50 -mx-4 px-4 transition-colors rounded-xl">
                                <div class="w-14 h-20 rounded-md shadow-sm overflow-hidden flex-shrink-0 cover-4 flex items-center justify-center relative">
                                     <div class="absolute inset-0 bg-white/20"></div>
                                     <i class="ph-fill ph-book text-white/50 text-2xl relative z-10"></i>
                                </div>
                                <div class="ml-4 flex-grow">
                                    <h3 class="font-bold text-gray-800 text-[15px] leading-tight mb-1 group-hover:text-primary transition-colors">지적 대화를 위한<br>넓고 얕은 지식</h3>
                                    <p class="text-sm text-gray-400 mb-2">채사장</p>
                                    <span class="inline-block px-2.5 py-1 bg-gray-100 text-gray-600 text-xs font-semibold rounded-full">인문</span>
                                </div>
                                <i class="ph ph-caret-right text-gray-300 text-xl group-hover:text-primary transition-colors ml-2"></i>
                            </a>
                        </div>
                        
                    </div>
                </div>

            </div>
        </div>
    </main>

</body>
</html>
