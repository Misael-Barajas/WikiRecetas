const next = document.querySelector('.next'); 
            const prev = document.querySelector('.prev');

            next.addEventListener('click', function() {
                const items = document.querySelectorAll('.item');
                document.querySelector('.slide').appendChild(items[0]);
            });

            prev.addEventListener('click', function() {
                const items = document.querySelectorAll('.item');
                document.querySelector('.slide').prepend(items[items.length - 1]);
            });