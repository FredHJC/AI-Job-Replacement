document.addEventListener('alpine:init', () => {
    Alpine.data('resultPage', () => ({
        expandedDim: null,
        result: null,
        loaded: false,
        generating: false,
        showImageModal: false,
        imageDataUrl: '',
        init() {
            const raw = sessionStorage.getItem('quizResult');
            if (!raw) { window.location.href = '/'; return; }
            this.result = JSON.parse(raw);
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
        riskTagInline(score) {
            if (score >= 6) return 'background:#FEF2F2;color:#DC2626;border:1px solid #FECACA';
            if (score >= 4) return 'background:#FFF7ED;color:#E97316;border:1px solid #FED7AA';
            if (score === 3) return 'background:#FFFBEB;color:#D97706;border:1px solid #FDE68A';
            if (score === 2) return 'background:#E8F4F4;color:#2A6B6B;border:1px solid #A7D8D8';
            return 'background:#ECFDF5;color:#059669;border:1px solid #A7F3D0';
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
            this.generating = true;
            try {
                await this.$nextTick();
                const card = this.buildShareCard();
                document.body.appendChild(card);

                const canvas = await html2canvas(card, {
                    scale: 2,
                    backgroundColor: '#FAFAF5',
                    useCORS: true,
                    logging: false,
                });
                document.body.removeChild(card);

                this.imageDataUrl = canvas.toDataURL('image/png');
                this.generating = false;

                const shared = await this.tryNativeShare();
                if (!shared) {
                    this.showImageModal = true;
                }
            } catch (err) {
                console.error('Image generation failed:', err);
                this.generating = false;
                this.copyText();
            }
        },
        async tryNativeShare() {
            try {
                const blob = await (await fetch(this.imageDataUrl)).blob();
                const file = new File([blob], 'ai-risk-result.png', { type: 'image/png' });
                if (navigator.canShare && navigator.canShare({ files: [file] })) {
                    await navigator.share({
                        files: [file],
                        title: this.lang === 'zh' ? '我的AI替代风险测试结果' : 'My AI Replacement Risk',
                    });
                    return true;
                }
            } catch (err) {
                if (err.name !== 'AbortError') console.log('Share API unavailable:', err);
            }
            return false;
        },
        downloadImage() {
            const link = document.createElement('a');
            link.href = this.imageDataUrl;
            link.download = 'ai-risk-result.png';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        },
        async copyText() {
            const text = this.lang === 'zh'
                ? `我的AI替代风险测试结果：${this.result.total_score}分（${this.result.risk_label_zh}）\n职业：${this.result.job_name_zh}`
                : `My AI Risk Score: ${this.result.total_score} (${this.result.risk_label_en})\nJob: ${this.result.job_name_en}`;
            await navigator.clipboard.writeText(text);
        },
        buildShareCard() {
            const isZh = this.lang === 'zh';
            const r = this.result;
            const color = this.gaugeColor;
            const isOverride = r.risk_level === 'override';

            let dimensionHtml = '';
            if (!isOverride) {
                const labels = isZh
                    ? ['职业类型', '产出形式', '知识类型', '委托能力', '容错率', '职级定位']
                    : ['Job Type', 'Output', 'Knowledge', 'Delegation', 'Tolerance', 'Level'];
                r.breakdown.forEach((score, idx) => {
                    const tag = this.riskTag(score);
                    const tagStyle = this.riskTagInline(score);
                    dimensionHtml += "<div style='display:flex;align-items:center;justify-content:space-between;padding:6px 0'>"
                        + "<span style='font-size:12px;color:#6B6B6B'>" + labels[idx] + "</span>"
                        + "<span style='font-size:11px;font-weight:500;padding:3px 10px;border-radius:20px;" + tagStyle + "'>" + tag + "</span>"
                        + "</div>";
                });
            }

            const card = document.createElement('div');
            card.style.cssText = "position:fixed;left:-9999px;top:0;width:375px;padding:40px 28px;background:#FAFAF5;font-family:'Noto Sans SC','Inter',system-ui,sans-serif";

            let html = '<div style="text-align:center;margin-bottom:24px">';
            if (isOverride) {
                html += '<div style="width:64px;height:64px;border-radius:50%;background:#F5F0EB;display:inline-flex;align-items:center;justify-content:center;margin-bottom:16px">'
                    + '<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#6B6B6B" stroke-width="1.5"><path d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>'
                    + '</div>';
            } else {
                html += '<div style="font-size:48px;font-weight:700;color:' + color + ";font-family:'Noto Serif SC',Georgia,serif\">" + r.total_score + '</div>'
                    + '<div style="font-size:13px;color:#6B6B6B;margin-top:2px">/ 100</div>';
            }
            html += '<div style="font-size:13px;color:#6B6B6B;margin-top:12px">' + (isZh ? r.job_name_zh : r.job_name_en) + '</div>'
                + '<div style="font-size:20px;font-weight:700;color:' + (isOverride ? '#6B6B6B' : color) + ";font-family:'Noto Serif SC',Georgia,serif;line-height:1.4\">" + (isZh ? r.risk_label_zh : r.risk_label_en) + '</div>'
                + '</div>';

            html += '<div style="background:white;border:1px solid #E5E0DA;border-radius:16px;padding:20px;margin-bottom:16px">'
                + "<div style=\"font-size:15px;font-weight:700;margin-bottom:8px;font-family:'Noto Serif SC',Georgia,serif\">" + (isZh ? '分析与建议' : 'Analysis & Advice') + '</div>'
                + '<div style="font-size:13px;color:#3D3D3D;line-height:1.7;white-space:pre-line">' + (isZh ? r.advice_zh : r.advice_en) + '</div>'
                + '</div>';

            if (!isOverride) {
                html += '<div style="background:white;border:1px solid #E5E0DA;border-radius:16px;padding:20px;margin-bottom:16px">'
                    + "<div style=\"font-size:15px;font-weight:700;margin-bottom:12px;font-family:'Noto Serif SC',Georgia,serif\">" + (isZh ? '维度拆解' : 'Breakdown') + '</div>'
                    + dimensionHtml
                    + '</div>';
            }

            html += '<div style="text-align:center;font-size:11px;color:#A8A39D;margin-top:20px">'
                + (isZh ? '我的工作会被AI替代吗？— 测一测' : 'Will AI Replace My Job? — Take the quiz')
                + '</div>';

            card.innerHTML = html;
            return card;
        },
    }));
});
