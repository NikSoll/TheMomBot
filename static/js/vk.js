document.addEventListener('DOMContentLoaded', function() {
    console.log('vk.js загружен');
    // MAKE
    const addMaster = document.getElementById('add-master');
    if (addMaster) {
        addMaster.addEventListener('click', function() {
            const container = document.getElementById('masters-container');
            const template = document.getElementById('master-template');
            if (container && template) {
                const clone = template.content.cloneNode(true);
                container.appendChild(clone);
            }
        });
    }

    const addService = document.getElementById('add-service');
    if (addService) {
        addService.addEventListener('click', function() {
            const container = document.getElementById('services-container');
            const template = document.getElementById('service-template');
            if (container && template) {
                const clone = template.content.cloneNode(true);
                container.appendChild(clone);
            }
        });
    }

    // SHOP
    const addCategory = document.getElementById('add-category');
    if (addCategory) {
        addCategory.addEventListener('click', function() {
            const container = document.getElementById('categories-container');
            const template = document.getElementById('category-template');
            if (container && template) {
                const clone = template.content.cloneNode(true);
                container.appendChild(clone);
            }
        });
    }

    const addProduct = document.getElementById('add-product');
    if (addProduct) {
        addProduct.addEventListener('click', function() {
            const container = document.getElementById('products-container');
            const template = document.getElementById('product-template');
            if (container && template) {
                const clone = template.content.cloneNode(true);
                container.appendChild(clone);
            }
        });
    }

    // QUIZ
    const addQuestion = document.getElementById('add-question');
    if (addQuestion) {
        addQuestion.addEventListener('click', function() {
            const container = document.getElementById('questions-container');
            const template = document.getElementById('question-template');
            if (container && template) {
                const clone = template.content.cloneNode(true);
                container.appendChild(clone);
            }
        });
    }

    const addResult = document.getElementById('add-result');
    if (addResult) {
        addResult.addEventListener('click', function() {
            const container = document.getElementById('results-container');
            const template = document.getElementById('result-template');
            if (container && template) {
                const clone = template.content.cloneNode(true);
                container.appendChild(clone);
            }
        });
    }

    // SURVEY
    const addQuestionSurvey = document.getElementById('add-question-survey');
    if (addQuestionSurvey) {
        addQuestionSurvey.addEventListener('click', function() {
            const container = document.getElementById('questions-container-survey');
            const template = document.getElementById('question-template');
            if (container && template) {
                const clone = template.content.cloneNode(true);
                container.appendChild(clone);
            }
        });
    }

    // MAILER
    const addGroup = document.getElementById('add-group');
    if (addGroup) {
        addGroup.addEventListener('click', function() {
            const container = document.getElementById('groups-container');
            const template = document.getElementById('group-template');
            if (container && template) {
                const clone = template.content.cloneNode(true);
                container.appendChild(clone);
            }
        });
    }

    const addTemplate = document.getElementById('add-template');
    if (addTemplate) {
        addTemplate.addEventListener('click', function() {
            const container = document.getElementById('templates-container');
            const template = document.getElementById('template-template');
            if (container && template) {
                const clone = template.content.cloneNode(true);
                container.appendChild(clone);
            }
        });
    }

    //удал
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('remove-item')) {
            const item = e.target.closest('.array-item, .master-item, .service-item, .product-item, .category-item, .question-item, .result-item, .group-item, .template-item');
            if (item) {
                item.remove();
            }
        }
    });
});