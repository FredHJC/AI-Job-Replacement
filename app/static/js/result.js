document.addEventListener('alpine:init', () => {
    Alpine.data('resultPage', () => ({
        expandedDim: null,
        result: null,
        resultId: null,
        loaded: false,
        generating: false,
        showImageModal: false,
        shareImageUrl: '',
        init() {
            // Prefer server-rendered data (permalink), fall back to sessionStorage
            if (window.__SERVER_RESULT__) {
                this.result = window.__SERVER_RESULT__;
                const match = window.location.pathname.match(/\/result\/([^/]+)/);
                if (match) this.resultId = match[1];
            } else {
                const raw = sessionStorage.getItem('quizResult');
                if (!raw) { window.location.href = '/'; return; }
                this.result = JSON.parse(raw);
                this.resultId = this.result.result_id || null;
            }
            setTimeout(() => this.loaded = true, 100);
        },
        get gaugeOffset() {
            if (!this.result) return 283;
            const pct = this.result.total_score / 100;
            return 283 - (283 * pct);
        },
        get gaugeColor() {
            if (!this.result) return '#6B6B6B';
            const s = this.result.total_score;
            if (s >= 86) return '#DC2626';
            if (s >= 67) return '#E97316';
            if (s >= 38) return '#F59E0B';
            if (s >= 15) return '#2A6B6B';
            return '#059669';
        },
        get riskLabel() {
            if (!this.result) return '';
            return this.lang === 'zh' ? this.result.risk_label_zh : this.result.risk_label_en;
        },
        get advice() {
            if (!this.result) return '';
            return this.lang === 'zh' ? this.result.advice_zh : this.result.advice_en;
        },
        get jobName() {
            if (!this.result) return '';
            return this.lang === 'zh' ? this.result.job_name_zh : this.result.job_name_en;
        },
        questionLabels(idx) {
            const zh = ['职业类型', '产出形式', '知识类型', '委托能力', '容错率', '职级定位'];
            const en = ['Job Type', 'Output Form', 'Knowledge Type', 'Delegation', 'Error Tolerance', 'Career Level'];
            return this.lang === 'zh' ? zh[idx] : en[idx];
        },
        riskTag(score) {
            if (score >= 6) return this.lang === 'zh' ? '高危' : 'High Risk';
            if (score >= 4) return this.lang === 'zh' ? '中高风险' : 'Med-High';
            if (score === 3) return this.lang === 'zh' ? '中等' : 'Moderate';
            if (score === 2) return this.lang === 'zh' ? '较低' : 'Low';
            return this.lang === 'zh' ? '安全' : 'Safe';
        },
        riskTagColor(score) {
            if (score >= 6) return 'bg-red-50 text-red-600 border-red-200';
            if (score >= 4) return 'bg-orange-50 text-orange-600 border-orange-200';
            if (score === 3) return 'bg-amber-50 text-amber-600 border-amber-200';
            if (score === 2) return 'bg-teal-50 text-teal-600 border-teal-200';
            return 'bg-emerald-50 text-emerald-600 border-emerald-200';
        },
        getExplanation(dimIdx, score) {
            const dim = window.__EXPLANATIONS__[String(dimIdx)];
            if (!dim) return null;
            let tier;
            if (dimIdx === 0) {
                tier = score >= 5 ? 'high' : score >= 3 ? 'medium' : 'low';
            } else {
                tier = score >= 4 ? 'high' : score >= 2 ? 'medium' : 'low';
            }
            const tierData = dim.tiers[tier];
            return {
                title: this.lang === 'zh' ? dim.title_zh : dim.title_en,
                text: this.lang === 'zh' ? tierData.zh : tierData.en,
            };
        },
        toggleDim(idx) {
            this.expandedDim = this.expandedDim === idx ? null : idx;
        },
        async generateImage() {
            if (!this.resultId) {
                await this.copyText();
                return;
            }

            this.generating = true;
            const imageUrl = `/result/${this.resultId}/image.png?lang=${this.lang}`;

            try {
                const resp = await fetch(imageUrl);
                const blob = await resp.blob();
                const file = new File([blob], 'ai-risk-result.png', { type: 'image/png' });

                // Try native share (works on iOS 15+, Android)
                if (navigator.canShare && navigator.canShare({ files: [file] })) {
                    try {
                        await navigator.share({
                            files: [file],
                            title: this.lang === 'zh' ? '我的AI替代风险测试结果' : 'My AI Replacement Risk',
                        });
                        this.generating = false;
                        return;
                    } catch (e) {
                        if (e.name === 'AbortError') { this.generating = false; return; }
                    }
                }

                // Fallback: show modal with real server URL (iOS long-press save works)
                this.shareImageUrl = imageUrl;
                this.generating = false;
                this.showImageModal = true;
            } catch (err) {
                console.error('Image share failed:', err);
                this.generating = false;
                await this.copyText();
            }
        },
        async copyText() {
            const url = this.resultId ? `${window.location.origin}/result/${this.resultId}` : '';
            const text = this.lang === 'zh'
                ? `我的AI替代风险测试结果：${this.result.total_score}分（${this.result.risk_label_zh}）\n职业：${this.result.job_name_zh}${url ? '\n' + url : ''}`
                : `My AI Risk Score: ${this.result.total_score} (${this.result.risk_label_en})\nJob: ${this.result.job_name_en}${url ? '\n' + url : ''}`;
            await navigator.clipboard.writeText(text);
        },
    }));
});
