class HabitHeatmap {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.cal = null;
    }

    async loadHabitData(habitId, days = 365) {
        try {
            const response = await fetch(`/tracking/${habitId}/heatmap?days=${days}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            
            this.renderHeader(data);
            this.renderStats(data);
            this.renderHeatmap(data.heatmap_data, days);
        } catch (error) {
            console.error('Ошибка загрузки данных:', error);
            this.showError('Не удалось загрузить данные привычки');
        }
    }

    renderHeader(data) {
        const header = document.createElement('div');
        header.className = 'heatmap-header';
        header.innerHTML = `
            <h2>${this.escapeHtml(data.habit_name)}</h2>
            <p class="habit-description">${this.escapeHtml(data.habit_description || 'Нет описания')}</p>
            <div class="goal-progress">
                <span class="progress-label">Прогресс:</span>
                <span class="progress-value">${data.progress}${data.goal ? `/${data.goal}` : ''} дней</span>
                ${data.goal ? `<span class="goal-percentage">${Math.round((data.progress/data.goal)*100)}%</span>` : ''}
            </div>
        `;
        this.container.appendChild(header);
    }

    renderStats(data) {
        const statsContainer = document.createElement('div');
        statsContainer.className = 'heatmap-stats';
        
        const stats = [
            { label: 'Текущая серия', value: `${data.current_streak} ${this.pluralize(data.current_streak, 'день', 'дня', 'дней')}` },
            { label: 'Лучшая серия', value: `${data.longest_streak} ${this.pluralize(data.longest_streak, 'день', 'дня', 'дней')}` },
            { label: 'Всего выполнений', value: data.total_completions },
            { label: 'Выполнение', value: `${data.completion_rate}%` }
        ];
        
        stats.forEach(stat => {
            const card = document.createElement('div');
            card.className = 'stat-card';
            card.innerHTML = `
                <div class="stat-label">${stat.label}</div>
                <div class="stat-value">${stat.value}</div>
            `;
            statsContainer.appendChild(card);
        });
        
        this.container.appendChild(statsContainer);
    }

    renderHeatmap(heatmapData, days) {
        // Создаём контейнер для тепловой карты
        const heatmapContainer = document.createElement('div');
        heatmapContainer.id = 'cal-heatmap';
        heatmapContainer.style.margin = '20px 0';
        this.container.appendChild(heatmapContainer);

        // Преобразуем данные в формат для CalHeatmap
        // CalHeatmap ожидает { "timestamp": value, ... }
        const formattedData = {};
        for (const [dateStr, value] of Object.entries(heatmapData)) {
            const timestamp = new Date(dateStr).getTime() / 1000; // в секунды
            formattedData[timestamp] = value;
        }

        // Инициализируем CalHeatmap
        this.cal = new CalHeatmap();
        
        // Опции для тепловой карты
        const options = {
            data: {
                source: formattedData,
                type: 'json',
                x: (d) => d[0],  // timestamp
                y: (d) => d[1]   // значение
            },
            date: {
                start: new Date(Date.now() - (days-1) * 24 * 60 * 60 * 1000),
                end: new Date()
            },
            range: Math.ceil(days / 7), // количество недель
            domain: {
                type: 'month',
                gutter: 10,
                label: { text: 'MMM', textAlign: 'start', position: 'top' }
            },
            subDomain: {
                type: 'day',
                width: 15,
                height: 15,
                gutter: 2
            },
            scale: {
                color: {
                    type: 'linear',
                    range: ['#ebedf0', '#9be9a8', '#40c463', '#30a14e', '#216e39'],
                    domain: [0, 1, 2, 3, 4],
                    interpolate: (t) => t // линейная интерполяция
                }
            },
            legend: [1, 2, 3, 4],
            tooltip: {
                text: (date, value) => {
                    const dateStr = date.toLocaleDateString('ru-RU', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric'
                    });
                    
                    if (value === 1) {
                        return `✅ ${dateStr} — выполнено`;
                    }
                    return `❌ ${dateStr} — не выполнено`;
                }
            },
            itemSelector: '#cal-heatmap'
        };

        this.cal.paint(options);

        // Добавляем легенду
        this.renderLegend();
    }

    renderLegend() {
        const legend = document.createElement('div');
        legend.className = 'heatmap-legend';
        legend.innerHTML = `
            <span>Меньше</span>
            <div class="legend-colors">
                <div class="legend-color" style="background: #ebedf0;"></div>
                <div class="legend-color" style="background: #9be9a8;"></div>
                <div class="legend-color" style="background: #40c463;"></div>
                <div class="legend-color" style="background: #30a14e;"></div>
                <div class="legend-color" style="background: #216e39;"></div>
            </div>
            <span>Больше</span>
        `;
        this.container.appendChild(legend);
    }

    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        this.container.appendChild(errorDiv);
    }

    escapeHtml(text) {
        if (!text) return text;
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    pluralize(count, one, few, many) {
        const mod10 = count % 10;
        const mod100 = count % 100;
        
        if (mod100 >= 11 && mod100 <= 19) {
            return many;
        }
        if (mod10 === 1) {
            return one;
        }
        if (mod10 >= 2 && mod10 <= 4) {
            return few;
        }
        return many;
    }
}

// Класс для отображения нескольких тепловых карт
class MultiHabitHeatmap {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
    }

    async loadAllHabits(days = 90) {
        try {
            const response = await fetch(`/tracking/heatmaps?days=${days}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            
            data.habits.forEach(habit => {
                this.renderHabitCard(habit, days);
            });
        } catch (error) {
            console.error('Ошибка загрузки привычек:', error);
            this.container.innerHTML = '<p class="error-message">Ошибка загрузки данных</p>';
        }
    }

    renderHabitCard(habit, days) {
        const card = document.createElement('div');
        card.className = 'habit-card';
        card.style.borderLeft = `4px solid ${habit.color}`;
        
        // Заголовок
        const header = document.createElement('div');
        header.className = 'habit-card-header';
        header.innerHTML = `
            <h3>${this.escapeHtml(habit.habit_name)}</h3>
            <div class="habit-card-stats">
                <span class="streak">🔥 ${habit.current_streak}</span>
                <span class="total">📊 ${habit.total_completions}</span>
            </div>
        `;
        card.appendChild(header);
        
        // Контейнер для тепловой карты этой привычки
        const heatmapDiv = document.createElement('div');
        heatmapDiv.className = 'habit-mini-heatmap';
        heatmapDiv.id = `heatmap-${habit.habit_id}`;
        card.appendChild(heatmapDiv);
        
        this.container.appendChild(card);
        
        // Рендерим тепловую карту для этой привычки
        this.renderMiniHeatmap(heatmapDiv.id, habit.heatmap_data, days, habit.color);
    }

    renderMiniHeatmap(containerId, heatmapData, days, baseColor) {
        // Преобразуем данные
        const formattedData = {};
        for (const [dateStr, value] of Object.entries(heatmapData)) {
            const timestamp = new Date(dateStr).getTime() / 1000;
            formattedData[timestamp] = value;
        }

        // Создаём оттенки на основе базового цвета
        const colors = this.generateColorScale(baseColor);

        const cal = new CalHeatmap();
        cal.paint({
            data: {
                source: formattedData,
                type: 'json',
                x: (d) => d[0],
                y: (d) => d[1]
            },
            date: {
                start: new Date(Date.now() - (days-1) * 24 * 60 * 60 * 1000),
                end: new Date()
            },
            range: Math.ceil(days / 7),
            domain: { type: 'month', gutter: 5 },
            subDomain: { type: 'day', width: 10, height: 10, gutter: 1 },
            scale: {
                color: {
                    type: 'linear',
                    range: ['#f0f0f0', colors[0], colors[1], colors[2], colors[3]],
                    domain: [0, 1, 2, 3, 4]
                }
            },
            legend: [1, 2, 3, 4],
            tooltip: false,
            itemSelector: `#${containerId}`
        });
    }

    generateColorScale(baseColor) {
        // Из HSL строки "hsl(137, 70%, 50%)" получаем оттенки
        const match = baseColor.match(/hsl\((\d+),/);
        if (!match) return ['#9be9a8', '#40c463', '#30a14e', '#216e39'];
        
        const hue = parseInt(match[1]);
        return [
            `hsl(${hue}, 70%, 85%)`, // очень светлый
            `hsl(${hue}, 70%, 70%)`, // светлый
            `hsl(${hue}, 70%, 50%)`, // основной
            `hsl(${hue}, 70%, 35%)`  // тёмный
        ];
    }

    escapeHtml(text) {
        if (!text) return text;
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}