class HabitHeatmap {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.chart = null;
    }

    async loadHabitData(habitId, days = 365) {
        try {
            const response = await fetch(`/tracking/main/${habitId}/heatmap?days=${days}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            
            this.renderHeader(data);
            this.renderStats(data);
            this.renderHeatmap(data.heatmap_data, data.habit_name);
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

    renderHeatmap(heatmapData, habitName) {
        const heatmapContainer = document.createElement('div');
        heatmapContainer.className = 'anychart-heatmap-container';
        heatmapContainer.id = `heatmap-${Date.now()}`;
        heatmapContainer.style.height = '350px';
        heatmapContainer.style.width = '100%';
        this.container.appendChild(heatmapContainer);

        const dates = Object.keys(heatmapData).sort();
        if (dates.length === 0) return;
        
        const startDate = new Date(dates[0]);
        const endDate = new Date(dates[dates.length - 1]);
        
        const chartData = [];
        
        let currentDate = new Date(startDate);
        while (currentDate <= endDate) {
            const dateStr = currentDate.toISOString().split('T')[0];
            
            let dayOfWeek = currentDate.getDay() - 1;
            if (dayOfWeek < 0) dayOfWeek = 6;
            
            const weekNumber = Math.floor((currentDate - startDate) / (7 * 24 * 60 * 60 * 1000));
            
            chartData.push([
                weekNumber,
                dayOfWeek,
                heatmapData[dateStr] || 0
            ]);
            
            currentDate.setDate(currentDate.getDate() + 1);
        }

        this.chart = anychart.heatMap(chartData);
        
        const xAxis = this.chart.xAxis();
        xAxis.orientation('bottom');
        xAxis.title('Недели');
        xAxis.labels().enabled(true);
        xAxis.labels().fontSize(11);
        xAxis.labels().format(function() {
            return `W${this.value + 1}`;
        });
        
        const yAxis = this.chart.yAxis();
        yAxis.orientation('left');
        yAxis.title('День недели');
        yAxis.labels().enabled(true);
        yAxis.labels().fontSize(11);
        
        const weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];
        yAxis.labels().format(function() {
            return weekdays[this.value] || '';
        });
        
        this.chart.title(habitName);
        
        const colorScale = anychart.scales.linearColor();
        colorScale.colors(['#ebedf0', '#9be9a8', '#40c463', '#30a14e', '#216e39']);
        this.chart.colorScale(colorScale);
        
        this.chart.labels().enabled(false);
        
        this.chart.tooltip().titleFormat(function() {
            const weekNum = this.x;
            const dayOfWeek = this.y;
            const date = new Date(startDate);
            date.setDate(date.getDate() + (weekNum * 7) + dayOfWeek);
            return date.toLocaleDateString('ru-RU', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
        });
        
        this.chart.tooltip().format(function() {
            return this.value === 1 ? '✅ Выполнено' : '❌ Не выполнено';
        });
        
        if (this.chart.legend) {
            this.chart.legend().enabled(true);
            this.chart.legend().position('bottom');
        }
        
        if (this.chart.colorRange) {
            this.chart.colorRange().enabled(true);
            this.chart.colorRange().length('15%');
        }
        
        this.chart.container(heatmapContainer.id);
        this.chart.draw();

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

class MultiHabitHeatmap {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.charts = [];
    }

    async loadAllHabits(days = 90) {
        try {
            const response = await fetch(`/tracking/main/heatmaps?days=${days}`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            this.container.innerHTML = '';
            
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
        card.style.borderLeft = `4px solid ${habit.color || '#0366d6'}`;
        
        const header = document.createElement('div');
        header.className = 'habit-card-header';
        header.innerHTML = `
            <h3>${this.escapeHtml(habit.habit_name)}</h3>
            <div class="habit-card-stats">
                <span class="streak">🔥 ${habit.current_streak || 0}</span>
                <span class="total">📊 ${habit.total_completions || 0}</span>
            </div>
        `;
        card.appendChild(header);
        
        const heatmapDiv = document.createElement('div');
        heatmapDiv.className = 'habit-mini-heatmap';
        const uniqueId = `heatmap-${habit.habit_id}-${Date.now()}`;
        heatmapDiv.id = uniqueId;
        card.appendChild(heatmapDiv);
        
        this.container.appendChild(card);
        
        if (habit.heatmap_data && Object.keys(habit.heatmap_data).length > 0) {
            this.renderMiniHeatmap(uniqueId, habit.heatmap_data, habit.habit_name);
        } else {
            heatmapDiv.innerHTML = '<p style="text-align: center; color: #999;">Нет данных</p>';
        }
    }

    renderMiniHeatmap(containerId, heatmapData, habitName) {
        try {
            const dates = Object.keys(heatmapData).sort();
            if (dates.length === 0) return;
            
            const startDate = new Date(dates[0]);
            const endDate = new Date(dates[dates.length - 1]);
            
            const chartData = [];
            let currentDate = new Date(startDate);
            
            while (currentDate <= endDate) {
                const dateStr = currentDate.toISOString().split('T')[0];
                let dayOfWeek = currentDate.getDay() - 1;
                if (dayOfWeek < 0) dayOfWeek = 6;
                
                const weekNumber = Math.floor((currentDate - startDate) / (7 * 24 * 60 * 60 * 1000));
                
                chartData.push([
                    weekNumber,
                    dayOfWeek,
                    heatmapData[dateStr] || 0
                ]);
                
                currentDate.setDate(currentDate.getDate() + 1);
            }

            const chart = anychart.heatMap(chartData);
            
            const xAxis = chart.xAxis();
            xAxis.orientation('bottom');
            xAxis.labels().enabled(true);
            xAxis.labels().fontSize(9);
            xAxis.labels().format(function() {
                return `W${this.value + 1}`;
            });
            
            const yAxis = chart.yAxis();
            yAxis.orientation('left');
            yAxis.labels().enabled(true);
            yAxis.labels().fontSize(9);
            
            const weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];
            yAxis.labels().format(function() {
                return weekdays[this.value] || '';
            });
            
            const colorScale = anychart.scales.linearColor();
            colorScale.colors(['#ebedf0', '#9be9a8', '#40c463', '#30a14e', '#216e39']);
            chart.colorScale(colorScale);
            
            chart.title(false);
            chart.labels().enabled(false);
            chart.legend().enabled(false);
            chart.tooltip().enabled(false);
            
            chart.container(containerId);
            chart.draw();
            
            this.charts.push(chart);
            
        } catch (error) {
            console.error('Ошибка при создании мини-тепловой карты:', error);
            const container = document.getElementById(containerId);
            if (container) {
                container.innerHTML = '<p style="color: red; text-align: center;">Ошибка отображения</p>';
            }
        }
    }

    escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

let singleHeatmap;
let multiHeatmap;

document.addEventListener('DOMContentLoaded', () => {
    const urlParts = window.location.pathname.split('/');
    const habitId = urlParts[urlParts.length - 1];
    
    singleHeatmap = new HabitHeatmap('single-habit-heatmap');
    multiHeatmap = new MultiHabitHeatmap('all-habits-heatmap');
    
    const days = parseInt(document.getElementById('period').value);
    
    if (habitId && !isNaN(habitId) && habitId !== 'heatmap') {
        singleHeatmap.loadHabitData(habitId, days);
    } else {
        document.getElementById('single-habit-heatmap').innerHTML = 
            '<p class="loading">Выберите привычку для просмотра детальной статистики</p>';
    }
    
    multiHeatmap.loadAllHabits(days);
});

function changePeriod() {
    const days = parseInt(document.getElementById('period').value);
    
    document.getElementById('single-habit-heatmap').innerHTML = '';
    document.getElementById('all-habits-heatmap').innerHTML = '';
    
    const urlParts = window.location.pathname.split('/');
    const habitId = urlParts[urlParts.length - 1];
    
    if (habitId && !isNaN(habitId) && habitId !== 'heatmap') {
        singleHeatmap.loadHabitData(habitId, days);
    }
    
    multiHeatmap.loadAllHabits(days);
}