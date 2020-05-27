import json
import csv
import re
import os


class WFA:
    
    project_name = ''
    path_json_report = ''
    path_output_csv = ''

    result_ids = set()
    dict_report = {}
    
    path_studio_cmd = ''
    path_working_dir = ''
    path_json_reports_dir = ''
    path_csv_reports_dir = ''

    def __create_dir(self, path_dir):
        if not(os.path.isdir(path_dir)):
            print('Creating directory: ' + path_dir)
            os.mkdir(path_dir)
        return path_dir

    def __setup_paths(self, path_working_dir):
        self.path_working_dir = self.__create_dir(path_working_dir)
        self.path_json_reports_dir = self.__create_dir(rf'{self.path_working_dir}\JsonReports')
        self.path_csv_reports_dir = self.__create_dir(rf'{self.path_working_dir}\CSVReports')

    def __init__(self, project_name, path_working_dir=rf'{os.environ["HOMEPATH"]}\Documents\WorkflowAnalyzer'):
        self.__setup_paths(path_working_dir)
        self.project_name = project_name

    def __get_process_name(self, path_project_json):
        project_name = ''
        with open(path_project_json, mode='r') as f:
            pj = f.read()
            dict_pj = json.loads(pj)
            project_name = dict_pj['name']
        return project_name

    def run_report(self, path_project, path_studio_cmd=r'C:\Program Files (x86)\UiPath\Studio'):
        self.project_name = self.__get_process_name(path_project)
        self.path_studio_cmd = path_studio_cmd
        file_analyzer = 'UiPath.Studio.CommandLine.exe'
        path_output_file= rf'{self.path_json_reports_dir}\out.json'
        cmd = f'{file_analyzer} analyze -p "{path_project}" > "{path_output_file}"'
        print("cmd line: " + cmd)
        path_cwd = os.getcwd()
        os.chdir(path_studio_cmd)
        cmd_status = os.system(cmd)
        print(f'cmd status: {cmd_status}')
        os.chdir(path_cwd)
        if cmd_status == 0:
            self.path_json_report = path_output_file
        else:
            raise Exception(f'Workflow analysis failed. Status code: {cmd_status}')
        return self.path_json_report

    def __read_json_report(self):
        print("Path report: " + self.path_json_report)
        with open(self.path_json_report, 'r', encoding='utf-8') as f:
            report = f.read()
        report = report.replace('#json', '').replace('\n', '')
        self.dict_report = json.loads(report)
        return self.dict_report

    def __get_result_ids(self):
        id_pattern = '^[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}-'
        reg_id = re.compile(id_pattern)

        for k in self.dict_report:
            id = reg_id.search(k)
            self.result_ids.add(id.group(0))
        return self.result_ids

    def __output_csv(self):
        headers = ['FilePath', 'ErrorCode', 'ErrorSeverity', 'Description', 'Recommendation']
        self.path_output_csv = self.path_csv_reports_dir + '\\' + self.project_name + '.csv'
        print('START OUTPUTING CSV...')
        with open(self.path_output_csv, mode='w', newline='') as fo:
            writer = csv.writer(fo, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            writer.writerow(headers)

            row = []
            for v in self.result_ids:
                row = []
                for h in headers:
                    try:
                        row.append(self.dict_report[v + h])
                    except Exception as err:
                        print(f'Value: {v} for header: {h} not found')
                        pass
                if row:
                    writer.writerow(row)
        return self.path_output_csv

    def parse_report(self, path_json_report):
        self.path_json_report = path_json_report
        self.__read_json_report()
        self.__get_result_ids()
        self.__output_csv()
        return self.path_output_csv


if __name__ == '__main__':
    #p = r'C:\Users\A0765287\Documents\Work\Scripts\wf_analyzer\outputDocuSignUpload.json'
    #w = WFA('xd')
    #pp = w.parse_report(p)
    #print(pp)
    pass



