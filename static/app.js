(function () {
    var root = document.documentElement;
    root.classList.add('js-animate');

    var themeToggle = document.getElementById('themeToggle');
    var savedTheme = localStorage.getItem('bk_theme');

    if (savedTheme === 'dark' || savedTheme === 'light') {
        root.setAttribute('data-theme', savedTheme);
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', function () {
            var current = root.getAttribute('data-theme') || 'light';
            var next = current === 'dark' ? 'light' : 'dark';
            root.setAttribute('data-theme', next);
            localStorage.setItem('bk_theme', next);
        });
    }

    var menuToggle = document.getElementById('menuToggle');
    var navGroup = document.getElementById('navGroup');

    if (menuToggle && navGroup) {
        menuToggle.addEventListener('click', function () {
            navGroup.classList.toggle('open');
        });
    }

    var revealNodes = document.querySelectorAll('.reveal');
    if ('IntersectionObserver' in window && revealNodes.length) {
        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('show');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12 });

        revealNodes.forEach(function (node) {
            observer.observe(node);
        });
    } else {
        revealNodes.forEach(function (node) {
            node.classList.add('show');
        });
    }

    var productGrid = document.getElementById('productGrid');
    var searchInput = document.getElementById('productSearch');
    var sortSelect = document.getElementById('productSort');

    var applyProductFilters = function () {
        if (!productGrid) {
            return;
        }

        var cards = Array.prototype.slice.call(productGrid.querySelectorAll('.product-card'));
        var query = searchInput ? searchInput.value.trim().toLowerCase() : '';
        var sort = sortSelect ? sortSelect.value : 'default';

        cards.forEach(function (card) {
            var name = card.getAttribute('data-name') || '';
            var desc = card.getAttribute('data-description') || '';
            var visible = !query || name.indexOf(query) > -1 || desc.indexOf(query) > -1;
            card.style.display = visible ? '' : 'none';
        });

        if (sort !== 'default') {
            cards.sort(function (a, b) {
                var aName = a.getAttribute('data-name') || '';
                var bName = b.getAttribute('data-name') || '';
                var aPrice = parseInt(a.getAttribute('data-price') || '0', 10);
                var bPrice = parseInt(b.getAttribute('data-price') || '0', 10);

                if (sort === 'low-high') {
                    return aPrice - bPrice;
                }
                if (sort === 'high-low') {
                    return bPrice - aPrice;
                }
                return aName.localeCompare(bName);
            });

            cards.forEach(function (card) {
                productGrid.appendChild(card);
            });
        }
    };

    if (searchInput) {
        searchInput.addEventListener('input', applyProductFilters);
    }
    if (sortSelect) {
        sortSelect.addEventListener('change', applyProductFilters);
    }

    var cartItems = document.querySelectorAll('.cart-item');
    var itemCount = document.getElementById('itemCount');
    var subTotal = document.getElementById('subTotal');
    var finalTotal = document.getElementById('finalTotal');

    var recalcCart = function () {
        if (!cartItems.length) {
            return;
        }

        var count = 0;
        var total = 0;

        cartItems.forEach(function (item) {
            var price = parseInt(item.getAttribute('data-price') || '0', 10);
            var qtyNode = item.querySelector('.qty-value');
            var qty = parseInt(qtyNode ? qtyNode.textContent : '1', 10);
            count += qty;
            total += price * qty;
        });

        if (itemCount) {
            itemCount.textContent = String(count);
        }
        if (subTotal) {
            subTotal.textContent = 'Rs. ' + total;
        }
        if (finalTotal) {
            finalTotal.textContent = 'Rs. ' + total;
        }
    };

    document.querySelectorAll('.qty-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var wrap = btn.closest('.qty-box');
            if (!wrap) {
                return;
            }

            var valueNode = wrap.querySelector('.qty-value');
            if (!valueNode) {
                return;
            }

            var currentQty = parseInt(valueNode.textContent || '1', 10);
            if (btn.getAttribute('data-action') === 'plus') {
                currentQty += 1;
            } else {
                currentQty = Math.max(1, currentQty - 1);
            }
            valueNode.textContent = String(currentQty);
            recalcCart();
        });
    });

    recalcCart();
})();
