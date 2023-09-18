<template>
<!--    <div>-->
<!--        <div class="header-body">-->
<!--            <el-form :inline="true" :model="queryParams" ref="queryParams">-->
<!--                <el-form-item>-->
<!--                    <el-button-->
<!--                            type="primary"-->
<!--                            icon="el-icon-plus"-->
<!--                            @click="addProject">-->
<!--                        创建项目-->
<!--                    </el-button>-->
<!--                </el-form-item>-->
<!--                <el-form-item prop="name" style="float: right">-->
<!--                    <el-input prefix-icon="el-icon-search"-->
<!--                              clearable type="name"-->
<!--                              v-model.trim="queryParams.name"-->
<!--                              placeholder="请输入项目名称"-->
<!--                              @keyup.enter.native="queryList"></el-input>-->
<!--                </el-form-item>-->
<!--            </el-form>-->
<!--        </div>-->
<!--        <div>-->
<!--            <el-row>-->
<!--                <el-col :span="6" v-for="(item) in tableData" :key="item.id">-->
<!--                    <div style="width: 95%; margin-top: 20px; margin-left: 5px; cursor: pointer">-->
<!--                        <el-card shadow="hover" @click.native="editProject(item)">-->
<!--                            <div class="card-meta-avatar">-->
<!--                                <span class="avatar avatar-image">-->
<!--                                  <img :src=item.avatar>-->
<!--                                </span>-->
<!--                            </div>-->
<!--                            <div class="card-detail">-->
<!--                                <div class="card-title">-->
<!--                                    <div style="font-size: 16px; font-weight: bold; color: rgb(65, 74, 105);">-->
<!--                                        {{item.name}}-->
<!--                                        <el-dropdown style="float: right; color: #b6c1d0">-->
<!--                                            <i class="el-icon-more"></i>-->
<!--                                            <el-dropdown-menu size="mini" slot="dropdown">-->
<!--                                                <el-dropdown-item @click.native="deleteProjectData(item)">-->
<!--                                                    <template slot-scope="scope">-->
<!--                                                        <i style="color: red" class="el-icon-delete"></i>-->
<!--                                                        <span>删除项目</span>-->
<!--                                                    </template>-->
<!--                                                </el-dropdown-item>-->
<!--                                            </el-dropdown-menu>-->
<!--                                        </el-dropdown>-->
<!--                                    </div>-->
<!--                                </div>-->
<!--                                <div class="card-description">{{item.desc}}</div>-->
<!--                                <div class="card-description">负责人：{{item.user.username}}</div>-->
<!--                                <div class="card-description">更新时间：{{parseTime(item.create_time)}}</div>-->
<!--                            </div>-->
<!--                        </el-card>-->
<!--                    </div>-->
<!--                </el-col>-->
<!--            </el-row>-->
<!--        </div>-->
<!--        <el-pagination-->
<!--                style="margin-top: 8px;"-->
<!--                @current-change="queryList"-->
<!--                :current-page.sync="queryParams.page"-->
<!--                :page-size="20"-->
<!--                :total="count"-->
<!--                layout="->, total, prev, pager, next, jumper">-->
<!--        </el-pagination>-->
<!--        <add-dialog v-model="addDialogVisible" :dialogData="rowData"></add-dialog>-->
<!--    </div>-->
</template>

<script lang="ts" setup>
    // import {parseTime} from '@/utils/index'
    // import {delProject, projectList, copyProject} from '@/api/api'
    // import addDialog from './components/addDialog.vue'
    // import editDialog from "./components/editProject.vue";
    //
    // export default {
    //     name: 'Project',
    //     components: {
    //         editDialog,
    //         addDialog
    //     },
    //     data() {
    //         return {
    //             queryParams: {
    //                 name: '',
    //                 page: 1
    //             },
    //             loading: false,
    //             tableData: null,
    //             tableLoading: false,
    //             count: null,
    //             rowData: null,
    //             addDialogVisible: false
    //         }
    //     },
    //     created() {
    //         this.queryList()
    //     },
    //
    //     methods: {
    //         parseTime,
    //
    //         queryList() {
    //             this.tableLoading = true;
    //             projectList({params: this.queryParams}).then((response) => {
    //                 this.tableLoading = false;
    //                 this.tableData = response.data.results;
    //                 this.count = response.data.count;
    //             }).catch((error) => {
    //                 console.log(error.response)
    //                 this.$message.error("获取项目列表数据失败;请重试！")
    //             })
    //         },
    //
    //         addProject(row) {
    //             this.rowData = row;
    //             this.addDialogVisible = true;
    //         },
    //
    //         editProject(row) {
    //             this.rowData = row;
    //             this.$router.push({
    //                 name: "projectDetail",
    //                 query: {id: row.id}
    //             });
    //         },
    //
    //         copyApi(row) {
    //             this.$confirm(`确认是否复制项目 - ${row.name}?`).then(_ => {
    //                 copyProject({id: row.id}).then((response) => {
    //                     if (response.status === 200) {
    //                         this.$message.success("复制项目成功");
    //                         this.queryList();
    //                     }
    //                 })
    //             }).catch(_ => {
    //                 this.$message.error("复制项目失败请重试");
    //             })
    //         },
    //
    //         deleteProjectData(row) {
    //             console.log(row)
    //             this.$confirm(`确认删除项目数据 - ${row.name}?`).then(_ => {
    //                 delProject({id: row.id}).then((response) => {
    //                     if (response.status === 204) {
    //                         this.$message.success("删除成功");
    //                         this.queryList();
    //                     }
    //                 })
    //             }).catch(_ => {
    //                 this.$message.error("项目删除失败请重试");
    //             })
    //         }
    //     }
    // }
</script>

<!--<style rel="stylesheet/scss" lang="scss" scoped>-->
<!--    /deep/ {-->
<!--        .el-input-number {-->
<!--            .el-input__inner {-->
<!--                text-align: left;-->
<!--            }-->
<!--        }-->
<!--    }-->

<!--    .el-form {-->
<!--        /deep/ .el-form-item&#45;&#45;small.el-form-item {-->
<!--            margin-bottom: 0;-->
<!--        }-->
<!--    }-->

<!--    .crud-opts {-->
<!--        padding: 4px 0;-->
<!--        display: -webkit-flex;-->
<!--        display: flex;-->
<!--        align-items: center;-->
<!--        margin-bottom: 10px;-->

<!--        .crud-opts-right {-->
<!--            margin-left: auto;-->
<!--        }-->
<!--    }-->

<!--    .el-tooltip__popper {-->
<!--        max-width: 20%;-->
<!--    }-->

<!--    .date-item {-->
<!--        height: 28px !important;-->
<!--        width: 230px !important;-->
<!--    }-->

<!--    .card-meta-avatar {-->
<!--        float: left;-->
<!--        padding-right: 16px-->
<!--    }-->

<!--    .avatar {-->
<!--        box-sizing: border-box;-->
<!--        margin: 0;-->
<!--        padding: 0;-->
<!--        color: rgba(0, 0, 0, .85);-->
<!--        font-size: 13px;-->
<!--        font-variant: tabular-nums;-->
<!--        line-height: 1.5715;-->
<!--        list-style: none;-->
<!--        font-feature-settings: "tnum", "tnum";-->
<!--        position: relative;-->
<!--        display: inline-block;-->
<!--        overflow: hidden;-->
<!--        color: #fff;-->
<!--        white-space: nowrap;-->
<!--        text-align: center;-->
<!--        vertical-align: middle;-->
<!--        background: #ccc;-->
<!--        width: 32px;-->
<!--        height: 32px;-->
<!--        line-height: 32px;-->
<!--        border-radius: 50%;-->
<!--    }-->

<!--    .avatar-image {-->
<!--        background: transparent;-->
<!--        width: 48px;-->
<!--        height: 48px;-->
<!--        line-height: 48px;-->
<!--        font-size: 18px;-->

<!--        img {-->
<!--            display: block;-->
<!--            width: 100%;-->
<!--            height: 100%;-->
<!--            object-fit: cover;-->
<!--        }-->
<!--    }-->

<!--    .card-detail {-->
<!--        overflow: hidden;-->
<!--    }-->

<!--    .card-description {-->
<!--        font-size: 13px;-->
<!--        color: rgba(0, 0, 0, .45);-->
<!--        margin-top: 15px;-->
<!--        clear: both-->
<!--    }-->
<!--</style>-->
