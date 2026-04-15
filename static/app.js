(function () {
    const body = document.body;
    const toggle = document.getElementById('themeToggle');
    const key = 'blipkart-theme';

    const applyTheme = (theme) => {
        body.classList.toggle('dark', theme === 'dark');
    };

    const saved = localStorage.getItem(key);
    applyTheme(saved === 'dark' ? 'dark' : 'light');

    if (toggle) {
        toggle.addEventListener('click', function () {
            const next = body.classList.contains('dark') ? 'light' : 'dark';
            applyTheme(next);
            localStorage.setItem(key, next);
        });
    }

    const reveals = document.querySelectorAll('.reveal');
    const revealObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('show');
                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.14 });

    reveals.forEach(function (node) {
        revealObserver.observe(node);
    });

    const search = document.getElementById('catalogSearch');
    if (search) {
        search.addEventListener('input', function () {
            const q = search.value.trim().toLowerCase();
            const cards = document.querySelectorAll('.product-card');
            cards.forEach(function (card) {
                const name = card.dataset.name || '';
                const desc = card.dataset.description || '';
                const show = !q || name.includes(q) || desc.includes(q);
                card.style.display = show ? '' : 'none';
            });
        });
    }

    const cartItems = document.querySelectorAll('.cart-item');
    if (cartItems.length) {
        const totalNode = document.getElementById('liveTotal');
        const itemCountNode = document.getElementById('itemCount');

        const recalc = function () {
            let total = 0;
            let count = 0;
            cartItems.forEach(function (item) {
                const qty = parseInt(item.querySelector('.qty-value').textContent, 10);
                const price = parseInt(item.dataset.price || '0', 10);
                total += qty * price;
                count += qty;
            });

            if (totalNode) {
                totalNode.textContent = '₹' + total;
            }
            if (itemCountNode) {
                itemCountNode.textContent = String(count);
            }
        };

        document.querySelectorAll('.qty-btn').forEach(function (btn) {
            btn.addEventListener('click', function () {
                const wrap = btn.closest('.qty-control');
                const valueNode = wrap.querySelector('.qty-value');
                let qty = parseInt(valueNode.textContent, 10);
                qty = btn.dataset.action === 'plus' ? qty + 1 : Math.max(1, qty - 1);
                valueNode.textContent = String(qty);
                recalc();
            });
        });

        recalc();
    }

    document.querySelectorAll('.toggle-pass').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const input = btn.closest('.password-wrap').querySelector('input');
            const hidden = input.type === 'password';
            input.type = hidden ? 'text' : 'password';
            btn.textContent = hidden ? 'Hide' : 'Show';
        });
    });
})();
