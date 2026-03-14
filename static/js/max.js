document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ max.js загружен');

    //унив
    function setupAddButton(btnId, containerId, templateId) {
        const btn = document.getElementById(btnId);
        if (btn) {
            btn.addEventListener('click', function() {
                const container = document.getElementById(containerId);
                const template = document.getElementById(templateId);
                if (container && template) {
                    const clone = template.content.cloneNode(true);
                    container.appendChild(clone);
                }
            });
        }
    }

    //MAKE
    setupAddButton('add-master', 'masters-container', 'master-template');
    setupAddButton('add-service', 'services-container', 'service-template');

    //SHOP
    setupAddButton('add-category', 'categories-container', 'category-template');
    setupAddButton('add-product', 'products-container', 'product-template');

    //QUIZ
    setupAddButton('add-question', 'questions-container', 'question-template');
    setupAddButton('add-result', 'results-container', 'result-template');

    //SURVEY
    setupAddButton('add-question-survey', 'questions-container-survey', 'question-template');

    //MAILER
    setupAddButton('add-group', 'groups-container', 'group-template');
    setupAddButton('add-template', 'templates-container', 'template-template');

    //удал
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('remove-item')) {
            const item = e.target.closest('.array-item, .master-item, .service-item, .product-item, .category-item, .question-item, .result-item, .group-item, .template-item');
            if (item) {
                item.remove();
            }
        }
    });

    //SURVEY показ/скрывать
    document.addEventListener('change', function(e) {
        if (e.target.name === 'question_type[]') {
            const item = e.target.closest('.question-item');
            if (!item) return;

            const optionsField = item.querySelector('.options-field');
            const scaleFields = item.querySelector('.scale-fields');

            if (optionsField) {
                optionsField.style.display =
                    (e.target.value === 'single' || e.target.value === 'multiple') ? 'block' : 'none';
            }
            if (scaleFields) {
                scaleFields.style.display =
                    e.target.value === 'scale' ? 'block' : 'none';
            }
        }
    });
});