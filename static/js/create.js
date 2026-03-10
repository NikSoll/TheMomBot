console.log('create.js загружен');
console.log('кнопки:', document.getElementById('add-category'));
document.addEventListener('DOMContentLoaded', function() {

    //MAKERS----------------------------------------------------
    const addMasterBtn = document.getElementById('add-master');
    if (addMasterBtn) {
        addMasterBtn.addEventListener('click', function() {
            const container = document.getElementById('masters-container');
            const template = document.getElementById('master-template');
            if (container && template) {
                container.appendChild(template.content.cloneNode(true));
            }
        });
    }

    const addServiceBtn = document.getElementById('add-service');
    if (addServiceBtn) {
        addServiceBtn.addEventListener('click', function() {
            const container = document.getElementById('services-container');
            const template = document.getElementById('service-template');
            if (container && template) {
                container.appendChild(template.content.cloneNode(true));
            }
        });
    }

    //SHOP-------------------------------------------------------
    const addCategoryBtn = document.getElementById('add-category');
    if (addCategoryBtn) {
        addCategoryBtn.addEventListener('click', function() {
            const container = document.getElementById('categories-container');
            const template = document.getElementById('category-template');
            if (container && template) {
                container.appendChild(template.content.cloneNode(true));
            }
        });
    }

    const addProductBtn = document.getElementById('add-product');
    if (addProductBtn) {
        addProductBtn.addEventListener('click', function() {
            const container = document.getElementById('products-container');
            const template = document.getElementById('product-template');
            if (container && template) {
                container.appendChild(template.content.cloneNode(true));
            }
        });
    }

    //QUIZ--------------------------
    const addQuestionBtn = document.getElementById('add-question');
    if (addQuestionBtn) {
        addQuestionBtn.addEventListener('click', function() {
            const container = document.getElementById('questions-container');
            const template = document.getElementById('question-template');
            if (container && template) {
                container.appendChild(template.content.cloneNode(true));
            }
        });
    }

    const addResultBtn = document.getElementById('add-result');
    if (addResultBtn) {
        addResultBtn.addEventListener('click', function() {
            const container = document.getElementById('results-container');
            const template = document.getElementById('result-template');
            if (container && template) {
                container.appendChild(template.content.cloneNode(true));
            }
        });
    }

    //MAILER--------------------------------------------
    const addGroupBtn = document.getElementById('add-group');
    if (addGroupBtn) {
        addGroupBtn.addEventListener('click', function() {
            const container = document.getElementById('groups-container');
            const template = document.getElementById('group-template');
            if (container && template) {
                container.appendChild(template.content.cloneNode(true));
            }
        });
    }

    //УДАЛЕНИЕ----------------------------------------------
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('remove-item')) {
            const item = e.target.closest('.array-item, .master-item, .service-item, .product-item, .category-item, .question-item, .result-item, .group-item');
            if (item) item.remove();
        }
    });

    //SURVEY (спец логика)---------------------------------------------------------
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

    //GOOGLE SHEETS----------------------------------------------------
    const useSheets = document.getElementById('useSheets');
    if (useSheets) {
        useSheets.addEventListener('change', function() {
            const sheetsSettings = document.getElementById('sheets-settings');
            if (sheetsSettings) {
                sheetsSettings.style.display = this.value === 'true' ? 'block' : 'none';
            }
        });
    }
});
