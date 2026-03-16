document.addEventListener('alpine:init', () => {
    Alpine.data('quiz', () => ({
        // Data from server
        jobs: window.__QUIZ_DATA__.jobs,
        jobGroups: window.__QUIZ_DATA__.jobGroups,
        questions: window.__QUIZ_DATA__.questions,
        overrideJobs: window.__QUIZ_DATA__.overrideJobs,
        consistencyWarnings: window.__QUIZ_DATA__.consistencyWarnings,

        // State
        currentStep: 0,       // 0 = Q1 (job), 1-5 = Q2-Q6, 6 = submitting
        answers: {},           // { q1: jobId, q2: 'A', q3: 'B', ... }
        selectedJob: null,
        searchQuery: '',
        transitioning: false,
        openGroups: [],        // expanded accordion group IDs
        warningText: '',       // current warning modal text (empty = hidden)
        pendingAction: null,   // callback to execute if user confirms warning

        // Computed
        get totalSteps() { return 6; },

        get progress() {
            return Math.round((this.currentStep / this.totalSteps) * 100);
        },

        get progressText() {
            return `${this.currentStep + 1} / ${this.totalSteps}`;
        },

        get canGoBack() { return this.currentStep > 0; },

        // Accordion toggle
        toggleGroup(groupId) {
            const idx = this.openGroups.indexOf(groupId);
            if (idx >= 0) {
                this.openGroups.splice(idx, 1);
            } else {
                this.openGroups.push(groupId);
            }
        },

        // Job filtering
        filteredJobs(groupId) {
            const groupJobs = this.jobs.filter(j => j.group === groupId);
            if (!this.searchQuery.trim()) return groupJobs;
            const q = this.searchQuery.toLowerCase().trim();
            return groupJobs.filter(j =>
                j.name_zh.toLowerCase().includes(q) ||
                j.name_en.toLowerCase().includes(q) ||
                j.id.toLowerCase().includes(q)
            );
        },

        hasJobsInGroup(groupId) {
            return this.filteredJobs(groupId).length > 0;
        },

        // Actions
        selectJob(job) {
            this.selectedJob = job;
            this.answers.q1 = job.id;

            // Check if this is an override job — skip to submit immediately
            if (this.overrideJobs.includes(job.id)) {
                setTimeout(() => this.submitOverride(), 400);
                return;
            }

            setTimeout(() => this.goNext(), 400);
        },

        selectOption(qIdx, opt) {
            const key = `q${qIdx + 2}`;
            this.answers[key] = opt.label;

            // Check consistency warnings
            const warning = this.checkConsistency(qIdx + 2, opt.label);
            if (warning) {
                this.warningText = this.lang === 'zh' ? warning[0] : warning[1];
                this.pendingAction = () => this.goNext();
                return;
            }

            setTimeout(() => this.goNext(), 400);
        },

        // Check if answer is inconsistent with job group
        checkConsistency(questionId, answerLabel) {
            if (!this.selectedJob) return null;
            const group = this.selectedJob.group;
            const rules = this.consistencyWarnings[group];
            if (!rules) return null;
            for (const rule of rules) {
                if (rule[0] === questionId && rule[1] === answerLabel) {
                    return [rule[2], rule[3]];
                }
            }
            return null;
        },

        // Dismiss warning modal
        dismissWarning(confirmed) {
            if (confirmed && this.pendingAction) {
                const action = this.pendingAction;
                this.warningText = '';
                this.pendingAction = null;
                setTimeout(() => action(), 50);
            } else {
                // User wants to change answer — clear the last selection
                const qIdx = this.currentStep - 1;
                if (qIdx >= 0) {
                    const key = `q${qIdx + 2}`;
                    delete this.answers[key];
                }
                this.warningText = '';
                this.pendingAction = null;
            }
        },

        isOptionSelected(qIdx, label) {
            return this.answers[`q${qIdx + 2}`] === label;
        },

        goNext() {
            if (this.transitioning) return;
            if (this.currentStep < 5) {
                this.transitioning = true;
                this.currentStep++;
                setTimeout(() => {
                    this.transitioning = false;
                }, 500);
            } else {
                this.submit();
            }
        },

        goBack() {
            if (this.transitioning || this.currentStep === 0) return;
            this.transitioning = true;
            this.currentStep--;
            setTimeout(() => {
                this.transitioning = false;
            }, 500);
        },

        async submitOverride() {
            // For override jobs, send minimal answers to get the override result
            this.currentStep = 6;
            const payload = {
                job_id: this.answers.q1,
                q2: 'A', q3: 'A', q4: 'A', q5: 'A', q6: 'A', // dummy values
            };
            try {
                const resp = await fetch('/api/score', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload),
                });
                const data = await resp.json();
                sessionStorage.setItem('quizResult', JSON.stringify(data));
                window.location.href = '/result';
            } catch (err) {
                console.error('Submit error:', err);
                this.currentStep = 0;
            }
        },

        async submit() {
            this.currentStep = 6;
            const payload = {
                job_id: this.answers.q1,
                q2: this.answers.q2,
                q3: this.answers.q3,
                q4: this.answers.q4,
                q5: this.answers.q5,
                q6: this.answers.q6,
            };

            try {
                const resp = await fetch('/api/score', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload),
                });
                const data = await resp.json();
                sessionStorage.setItem('quizResult', JSON.stringify(data));
                window.location.href = '/result';
            } catch (err) {
                console.error('Submit error:', err);
                this.currentStep = 5;
            }
        },
    }));
});
