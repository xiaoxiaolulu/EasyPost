// 文档参考：https://cz-git.qbb.sh/zh/config/
// cz.config.js  kk
/** @type {import('cz-git').CommitizenGitOptions} */
module.exports = {
    ignores: [commit => commit.includes("init")],
    extends: ["@commitlint/config-conventional"],
    // alias: { fd: 'docs: fix typos' },
    // messages: {
    //     type: 'Select the type of change that you\'re committing:',
    //     scope: 'Denote the SCOPE of this change (optional):',
    //     customScope: 'Denote the SCOPE of this chang     e:',
    //     subject: 'Write a SHORT, IMPERATIVE tense description of the change:\n',
    //     body: 'Provide a LONGER description of the change (optional). Use "|" to break new line:\n',
    //     breaking: 'List any BREAKING CHANGES (optional). Use "|" to break new line:\n',
    //     footerPrefixsSelect: 'Select the ISSUES type of changeList by this change (optional):',
    //     customFooterPrefixs: 'Input ISSUES prefix:',
    //     footer: 'List any ISSUES by this change. E.g.: #31, #34:\n',
    //     confirmCommit: 'Are you sure you want to proceed with the commit above?'
    // },
    prompt: {
        // 中英文对照版
        messages: {
            type: '选择你要提交的类型 :',
            scope: '选择一个提交范围（可选）:',
            customScope: '请输入自定义的提交范围 :',
            subject: '填写简短精炼的变更描述 :\n',
            body: '填写更加详细的变更描述（可选）。使用 "|" 换行 :\n',
            breaking: '列举非兼容性重大的变更（可选）。使用 "|" 换行 :\n',
            footerPrefixesSelect: '选择关联issue前缀（可选）:',
            customFooterPrefix: '输入自定义issue前缀 :',
            footer: '列举关联issue (可选) 例如: #31, #I3244 :\n',
            confirmCommit: '是否提交或修改commit ?'
        },
        types: [
            { value: '特性', name: '特性:     新增功能' },
            { value: '修复', name: '修复:     修复缺陷' },
            { value: '文档', name: '文档:     文档变更' },
            { value: '格式', name: '格式:     代码格式（不影响功能，例如空格、分号等格式修正）' },
            { value: '重构', name: '重构:     代码重构（不包括 bug 修复、功能新增）' },
            { value: '性能', name: '性能:     性能优化' },
            { value: '测试', name: '测试:     添加疏漏测试或已有测试改动' },
            { value: '构建', name: '构建:     构建流程、外部依赖变更（如升级 npm 包、修改 webpack 配置等）' },
            { value: '集成', name: '集成:     修改 CI 配置、脚本' },
            { value: '回退', name: '回退:     回滚 commit' },
            { value: '其他', name: '其他:     对构建过程或辅助工具和库的更改（不影响源文件、测试用例）' },

        ],
        // emptyScopesAlias: 'empty:      不填写',
        // customScopesAlias: 'custom:     自定义',

        useEmoji: true,
        // emojiAlign: 'center',
        themeColorCode: '',
        scopes: [],
        allowCustomScopes: true,
        allowEmptyScopes: true,
        customScopesAlign: 'bottom',
        customScopesAlias: 'custom',
        emptyScopesAlias: 'empty',
        upperCaseSubject: false,
        markBreakingChangeMode: false,
        allowBreakingChanges: ['feat', 'fix'],
        breaklineNumber: 100,
        breaklineChar: '|',
        skipQuestions: [],
        issuePrefixs: [{ value: 'closed', name: 'closed:   ISSUES has been processed' }],
        customIssuePrefixsAlign: 'top',
        emptyIssuePrefixsAlias: 'skip',
        customIssuePrefixsAlias: 'custom',
        allowCustomIssuePrefixs: true,
        allowEmptyIssuePrefixs: true,
        confirmColorize: true,
        maxHeaderLength: Infinity,
        maxSubjectLength: Infinity,
        minSubjectLength: 0,
        scopeOverrides: undefined,
        defaultBody: '',
        defaultIssues: '',
        defaultScope: '',
        defaultSubject: ''
    }

}
