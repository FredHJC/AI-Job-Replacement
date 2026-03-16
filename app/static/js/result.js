document.addEventListener('alpine:init', () => {
    Alpine.data('resultPage', () => ({
        expandedDim: null,
        result: null,
        loaded: false,
        generating: false,
        showImageModal: false,
        imageDataUrl: '',
        imageBlobUrl: '',
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

                // Create blob URL for iOS-friendly long-press save
                const blob = await (await fetch(this.imageDataUrl)).blob();
                if (this.imageBlobUrl) URL.revokeObjectURL(this.imageBlobUrl);
                this.imageBlobUrl = URL.createObjectURL(blob);

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

            // Build 2-column dimension grid
            let dimensionHtml = '';
            if (!isOverride) {
                const labels = isZh
                    ? ['职业类型', '产出形式', '知识类型', '委托能力', '容错率', '职级定位']
                    : ['Job Type', 'Output', 'Knowledge', 'Delegation', 'Tolerance', 'Level'];
                dimensionHtml = "<div style='display:flex;flex-wrap:wrap'>";
                r.breakdown.forEach((score, idx) => {
                    const tag = this.riskTag(score);
                    const tagStyle = this.riskTagInline(score);
                    const pad = idx % 2 === 0 ? 'padding-right:6px' : 'padding-left:6px';
                    dimensionHtml += "<div style='width:50%;display:flex;align-items:center;justify-content:space-between;padding:4px 0;box-sizing:border-box;" + pad + "'>"
                        + "<span style='font-size:11px;color:#6B6B6B;white-space:nowrap'>" + labels[idx] + "</span>"
                        + "<span style='font-size:10px;font-weight:500;padding:2px 8px 3px;border-radius:20px;display:inline-flex;align-items:center;justify-content:center;line-height:1.3;white-space:nowrap;" + tagStyle + "'>" + tag + "</span>"
                        + "</div>";
                });
                dimensionHtml += "</div>";
            }

            // 4:3 ratio card (width 375, height 500)
            const card = document.createElement('div');
            card.style.cssText = "position:fixed;left:-9999px;top:0;width:375px;height:500px;box-sizing:border-box;padding:28px 24px;background:#FAFAF5;font-family:'Noto Sans SC','Inter',system-ui,sans-serif;overflow:hidden";

            // Score header — compact
            let html = '<div style="text-align:center;margin-bottom:14px">';
            if (isOverride) {
                html += '<div style="width:48px;height:48px;border-radius:50%;background:#F5F0EB;display:inline-flex;align-items:center;justify-content:center;margin-bottom:8px">'
                    + '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#6B6B6B" stroke-width="1.5"><path d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>'
                    + '</div>';
            } else {
                html += '<div><span style="font-size:40px;font-weight:700;color:' + color + ";font-family:'Noto Serif SC',Georgia,serif\">" + r.total_score + '</span>'
                    + '<span style="font-size:13px;color:#6B6B6B;margin-left:4px">/ 100</span></div>';
            }
            html += '<div style="font-size:11px;color:#6B6B6B;margin-top:6px">' + (isZh ? r.job_name_zh : r.job_name_en) + '</div>'
                + '<div style="font-size:16px;font-weight:700;color:' + (isOverride ? '#6B6B6B' : color) + ";font-family:'Noto Serif SC',Georgia,serif;line-height:1.3;margin-top:2px\">" + (isZh ? r.risk_label_zh : r.risk_label_en) + '</div>'
                + '</div>';

            // Advice card — compact, single paragraph
            const adviceText = (isZh ? r.advice_zh : r.advice_en).replace(/\n\n/g, '\n');
            html += '<div style="background:white;border:1px solid #E5E0DA;border-radius:12px;padding:14px 16px;margin-bottom:10px">'
                + "<div style=\"font-size:13px;font-weight:700;margin-bottom:4px;font-family:'Noto Serif SC',Georgia,serif\">" + (isZh ? '分析与建议' : 'Analysis & Advice') + '</div>'
                + '<div style="font-size:11px;color:#3D3D3D;line-height:1.55;white-space:pre-line">' + adviceText + '</div>'
                + '</div>';

            // Dimension breakdown — 2-column grid
            if (!isOverride) {
                html += '<div style="background:white;border:1px solid #E5E0DA;border-radius:12px;padding:14px 16px;margin-bottom:10px">'
                    + "<div style=\"font-size:13px;font-weight:700;margin-bottom:8px;font-family:'Noto Serif SC',Georgia,serif\">" + (isZh ? '维度拆解' : 'Breakdown') + '</div>'
                    + dimensionHtml
                    + '</div>';
            }

            // Footer
            html += '<div style="text-align:center;font-size:10px;color:#A8A39D;margin-top:12px">'
                + (isZh ? '我的工作会被AI替代吗？— 测一测' : 'Will AI Replace My Job? — Take the quiz')
                + '</div>';

            card.innerHTML = html;
            return card;
        },
    }));
});
