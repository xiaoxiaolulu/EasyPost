<template>
    <div>
        <div class="container">
            <div>
                <el-form :inline="true" :model="queryParams" ref="queryParams">
                    <el-form-item>
                        <el-button
                                type="primary"
                                icon="el-icon-plus"
                                @click="addAddress">
                            创建环境
                        </el-button>
                    </el-form-item>
                    <el-form-item prop="name" style="float: right">
                        <el-input prefix-icon="el-icon-search"
                                  clearable type="name"
                                  v-model.trim="queryParams.name"
                                  placeholder="请输入项目名称"
                                  @keyup.enter.native="queryList"></el-input>
                    </el-form-item>
                </el-form>
            </div>
            <el-table :data="tableData"
                      border
                      v-loading="tableLoading"
                      element-loading-text="拼命加载中"
                      style="width: 100%">
                <el-table-column type="index" width="55" label="序号"></el-table-column>
                <el-table-column prop="env" label="环境">
                    <template slot-scope="scope">
                        <el-tag type="info">{{scope.row.env}}</el-tag>
                    </template>
                </el-table-column>
                <el-table-column prop="name" label="地址名称"></el-table-column>
                <el-table-column prop="host" label="服务地址">
                    <template slot-scope="scope">
                        <a :href="scope.row.host" target="_blank">{{scope.row.host | ellipsis}}</a>
                    </template>
                </el-table-column>
                <el-table-column label="操作" width="150px" align="center">
                    <template slot-scope="scope">
                        <el-button @click="editAddress(scope.row)" type="text">编辑</el-button>
                        <el-button @click="deleteAddress(scope.row)" type="text">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <!--分页组件-->
            <el-pagination
                    style="margin-top: 8px;"
                    @current-change="queryList"
                    :current-page.sync="queryParams.page"
                    :page-size="20"
                    :total="count"
                    layout="->, total, prev, pager, next, jumper">
            </el-pagination>
        </div>
        <add-dialog v-model="addDialogVisible" :dialogData="rowData"></add-dialog>
        <edit-dialog v-model="editDialogVisible" :dialogData='rowData'></edit-dialog>
    </div>
</template>

<script>
    import {parseTime} from '@/utils/index'
    import {AddressList, delAddress, envList} from '@/api/api'
    import addDialog from './components/addDialog.vue'
    import editDialog from "./components/editDialog.vue";

    export default {
        name: 'Address',
        components: {
            editDialog,
            addDialog
        },
        data() {
            return {
                queryParams: {
                    name: '',
                    page: 1
                },
                envCollections: [],
                loading: false,
                tableData: null,
                tableLoading: false,
                count: null,
                rowData: null,
                addDialogVisible: false,
                editDialogVisible: false,
            }
        },
        created() {
            this.queryEnvList()
        },
        filters: {
            ellipsis(value) {
                if (!value) {
                    return "";
                }
                if (value.length > 35) {
                    return value.slice(0, 35) + "...";
                } else {
                    return value;
                }
            }
        },
        methods: {
            parseTime,

            queryList() {
                this.tableLoading = true;
                AddressList({params: this.queryParams}).then((response) => {
                    this.tableLoading = false;
                    let list = response.data.results;
                    for (let i = 0; i < list.length; i++) {
                        let selectedName
                        //筛选出匹配数据，是对应数据的整个对象
                        selectedName = this.envCollections.find((item) => {
                            if (item.id === list[i].env) {
                                list[i].env = item.name
                            }
                        });
                    }
                    this.tableData = list;
                    this.count = response.data.count;
                }).catch((error) => {
                    console.log(error.response)
                    this.$message.error("获取地址列表数据失败;请重试!");
                })
            },

            queryEnvList() {
                envList().then((response) => {
                    this.envOption = [];
                    let envList = response.data.results
                    for (let i = 0; i < envList.length; i++) {
                        this.envCollections.push({
                            "name": envList[i]["name"],
                            "id": envList[i]["id"]
                        })
                    }
                    this.queryList()
                }).catch((error) => {
                    console.log(error.response)
                    this.$message.error("获取环境列表数据失败;请重试!");
                })
            },

            addAddress(row) {
                this.rowData = row;
                this.addDialogVisible = true;
            },

            editAddress(row) {
                this.rowData = row;
                this.editDialogVisible = true
            },


            deleteAddress(row) {
                this.$confirm(`确认删除地址数据 - ${row.name}?`).then(_ => {
                    delAddress({id: row.id}).then((response) => {
                        if (response.status === 204) {
                            this.$message.success("删除地址成功");
                            this.queryList();
                        }
                    })
                }).catch(_ => {
                    this.$message.error("删除失败请重试");
                })
            }
        }
    }
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    /deep/ {
        .el-input-number {
            .el-input__inner {
                text-align: left;
            }
        }
    }

    .el-tooltip__popper {
        max-width: 20%;
    }

    a {
        color: #1890ff;
        text-decoration: none;
        background-color: transparent;
        outline: none;
        cursor: pointer;
        transition: color .3s;
        -webkit-text-decoration-skip: objects;
    }
</style>
