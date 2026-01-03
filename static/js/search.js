// 搜索功能增强
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const searchForm = document.getElementById('search-form');
    const searchSuggestions = document.getElementById('search-suggestions');
    let debounceTimer;
    let isShowingSuggestions = false;
    
    if (searchInput && searchSuggestions) {
        // 确保初始状态是隐藏的
        searchSuggestions.style.display = 'none';
        
        // 输入时显示建议
        searchInput.addEventListener('input', function(e) {
            const query = e.target.value.trim();
            clearTimeout(debounceTimer);
            
            if (query.length >= 2) {
                debounceTimer = setTimeout(() => {
                    fetchSearchSuggestions(query);
                }, 300);
            } else {
                hideSuggestions();
            }
        });
        
        // 聚焦时显示最近搜索
        searchInput.addEventListener('focus', function() {
            if (this.value.length >= 2) {
                fetchSearchSuggestions(this.value);
            } else if (!isShowingSuggestions) {
                showRecentSearches();
            }
        });
        
        // 点击其他地方隐藏建议
        document.addEventListener('click', function(e) {
            if (!searchForm.contains(e.target) && 
                !searchSuggestions.contains(e.target)) {
                hideSuggestions();
            }
        });
        
        // 键盘导航
        searchInput.addEventListener('keydown', function(e) {
            const items = searchSuggestions.querySelectorAll('.search-suggestion-item');
            const activeItem = searchSuggestions.querySelector('.suggestion-active');
            let currentIndex = -1;
            
            if (activeItem) {
                currentIndex = Array.from(items).indexOf(activeItem);
            }
            
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                if (items.length > 0) {
                    if (!isShowingSuggestions) {
                        showRecentSearches();
                    }
                    const nextIndex = (currentIndex + 1) % items.length;
                    setActiveSuggestion(items[nextIndex]);
                }
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                if (items.length > 0) {
                    if (!isShowingSuggestions) {
                        showRecentSearches();
                    }
                    const prevIndex = (currentIndex - 1 + items.length) % items.length;
                    setActiveSuggestion(items[prevIndex]);
                }
            } else if (e.key === 'Escape') {
                hideSuggestions();
            } else if (e.key === 'Enter' && activeItem) {
                e.preventDefault();
                activeItem.click();
            }
        });
    }
    
    // 获取搜索建议
    function fetchSearchSuggestions(query) {
        fetch(`/home/search/suggest/?q=${encodeURIComponent(query)}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.results && data.results.length > 0) {
                    showSuggestions(data.results, query);
                } else {
                    showNoSuggestions(query);
                }
            })
            .catch(error => {
                console.error('搜索建议获取失败:', error);
                hideSuggestions();
            });
    }
    
    // 显示搜索建议
    function showSuggestions(results, query) {
        searchSuggestions.innerHTML = '';
        
        // 添加头部
        const header = document.createElement('div');
        header.className = 'suggestion-header';
        header.innerHTML = `
            <h4><i class="fas fa-search"></i> 搜索建议</h4>
            <span class="suggestion-count">${results.length}个结果</span>
        `;
        searchSuggestions.appendChild(header);
        
        // 添加结果项
        results.forEach(result => {
            const item = document.createElement('div');
            item.className = 'search-suggestion-item';
            item.innerHTML = `
                <div class="suggestion-icon">
                    <i class="fas fa-file-alt"></i>
                </div>
                <div class="suggestion-content">
                    <h4>${highlightText(result.resource_name, query)}</h4>
                    <p>${highlightText(result.resource_desc || '', query).substring(0, 60)}...</p>
                    <div class="suggestion-meta">
                        <span><i class="fas fa-user"></i> ${result.uploader}</span>
                        <span><i class="fas fa-download"></i> ${result.download_count} 下载</span>
                        <span class="suggestion-type">${result.resource_type}</span>
                    </div>
                </div>
            `;
            
            item.addEventListener('click', function(e) {
                e.stopPropagation();
                window.location.href = `/rsharing/detail/${result.id}/`;
                hideSuggestions();
            });
            
            item.addEventListener('mouseenter', function() {
                setActiveSuggestion(this);
            });
            
            searchSuggestions.appendChild(item);
        });
        
        // 添加关闭按钮
        const closeBtn = document.createElement('div');
        closeBtn.className = 'suggestion-close';
        closeBtn.innerHTML = '<i class="fas fa-times"></i> 关闭';
        closeBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            hideSuggestions();
        });
        searchSuggestions.appendChild(closeBtn);
        
        showSuggestionsContainer();
    }
    
    // 显示最近搜索
    function showRecentSearches() {
        const recentSearches = JSON.parse(localStorage.getItem('csp_recent_searches') || '[]');
        
        searchSuggestions.innerHTML = '';
        
        if (recentSearches.length > 0) {
            // 添加头部
            const header = document.createElement('div');
            header.className = 'suggestion-header';
            header.innerHTML = `
                <h4><i class="fas fa-history"></i> 最近搜索</h4>
            `;
            searchSuggestions.appendChild(header);
            
            // 添加快捷清除按钮
            const clearBtn = document.createElement('div');
            clearBtn.className = 'clear-recent';
            clearBtn.innerHTML = '<i class="fas fa-trash"></i> 清空历史';
            clearBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                localStorage.removeItem('csp_recent_searches');
                showRecentSearches();
            });
            searchSuggestions.appendChild(clearBtn);
            
            // 添加历史记录
            recentSearches.forEach(search => {
                const item = document.createElement('div');
                item.className = 'search-suggestion-item';
                item.innerHTML = `
                    <div class="suggestion-icon">
                        <i class="fas fa-history"></i>
                    </div>
                    <div class="suggestion-content">
                        <h4>${search}</h4>
                        <p>点击重新搜索</p>
                    </div>
                `;
                
                item.addEventListener('click', function(e) {
                    e.stopPropagation();
                    searchInput.value = search;
                    searchForm.submit();
                    hideSuggestions();
                });
                
                item.addEventListener('mouseenter', function() {
                    setActiveSuggestion(this);
                });
                
                searchSuggestions.appendChild(item);
            });
        } else {
            const emptyMessage = document.createElement('div');
            emptyMessage.className = 'no-suggestions';
            emptyMessage.innerHTML = `
                <div class="suggestion-icon">
                    <i class="fas fa-search"></i>
                </div>
                <div class="suggestion-content">
                    <h4>无最近搜索记录</h4>
                    <p>开始输入关键词进行搜索</p>
                </div>
            `;
            searchSuggestions.appendChild(emptyMessage);
        }
        
        showSuggestionsContainer();
    }
    
    // 显示无建议
    function showNoSuggestions(query) {
        searchSuggestions.innerHTML = `
            <div class="suggestion-header">
                <h4><i class="fas fa-search"></i> 搜索建议</h4>
            </div>
            <div class="no-suggestions">
                <div class="suggestion-icon">
                    <i class="fas fa-search"></i>
                </div>
                <div class="suggestion-content">
                    <h4>搜索 "${query}"</h4>
                    <p>没有找到相关建议，按回车键搜索</p>
                </div>
            </div>
            <div class="suggestion-close">
                <i class="fas fa-times"></i> 关闭
            </div>
        `;
        
        const closeBtn = searchSuggestions.querySelector('.suggestion-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                hideSuggestions();
            });
        }
        
        showSuggestionsContainer();
    }
    
   // 显示建议容器
    function showSuggestionsContainer() {
        searchSuggestions.classList.add('show');
        searchSuggestions.style.opacity = '0';
        searchSuggestions.style.transform = 'translateY(-10px)';
        
        // 强制重排
        searchSuggestions.offsetHeight;
        
        searchSuggestions.style.opacity = '1';
        searchSuggestions.style.transform = 'translateY(0)';
        isShowingSuggestions = true;
    }

    // 隐藏建议
    function hideSuggestions() {
        if (isShowingSuggestions) {
            searchSuggestions.style.opacity = '0';
            searchSuggestions.style.transform = 'translateY(-10px)';
            
            setTimeout(() => {
                searchSuggestions.classList.remove('show');
                isShowingSuggestions = false;
            }, 200);
        }
    }
    
    // 设置活动建议项
    function setActiveSuggestion(item) {
        // 移除所有活动状态
        searchSuggestions.querySelectorAll('.search-suggestion-item').forEach(i => {
            i.classList.remove('suggestion-active');
        });
        
        // 添加新的活动状态
        if (item) {
            item.classList.add('suggestion-active');
            // 确保活动项在视图中
            item.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
        }
    }
    
    // 高亮文本
    function highlightText(text, query) {
        if (!query || !text) return text;
        const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
        return text.replace(regex, '<span class="highlight">$1</span>');
    }
    
    // 保存搜索记录
    searchForm.addEventListener('submit', function(e) {
        const query = searchInput.value.trim();
        if (query) {
            saveSearchToHistory(query);
            hideSuggestions();
        }
    });
    
    // 输入框失去焦点时延迟隐藏建议
    searchInput.addEventListener('blur', function() {
        setTimeout(() => {
            const activeElement = document.activeElement;
            if (!searchSuggestions.contains(activeElement)) {
                hideSuggestions();
            }
        }, 200);
    });
    
    // 点击建议框时阻止隐藏
    searchSuggestions.addEventListener('mousedown', function(e) {
        e.preventDefault();
    });
    
    function saveSearchToHistory(query) {
        let recentSearches = JSON.parse(localStorage.getItem('csp_recent_searches') || '[]');
        
        // 移除重复项
        recentSearches = recentSearches.filter(s => s.toLowerCase() !== query.toLowerCase());
        
        // 添加到开头
        recentSearches.unshift(query);
        
        // 只保留最近10个
        if (recentSearches.length > 10) {
            recentSearches = recentSearches.slice(0, 10);
        }
        
        localStorage.setItem('csp_recent_searches', JSON.stringify(recentSearches));
    }
});