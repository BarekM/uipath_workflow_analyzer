import os
from tkinter import *
from tkinter import messagebox
import tkinter.filedialog as fd
import subprocess
from datetime import datetime

from wfa.wfa import WFA
import docs.config as cfg


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)        
        self.master = master

        # widget can take all window
        self.pack(fill=BOTH, expand=1)

        btn_analyze_project = Button(self, text="analyze project", command=self.analyze_project)
        btn_analyze_project.place(x=100, y=0)

        btn_parse_json_report = Button(self, text="parse json report", command=self.parse_json_report)
        btn_parse_json_report.place(x=100, y=50)

        btn_open_reports = Button(self, text="open output directory", command=self.open_reports)
        btn_open_reports.place(x=100, y=100)

    def analyze_project(self):
        path_uipath_projects = rf'{os.environ["HOMEPATH"]}\Documents\UiPath'
        path_project = fd.askopenfilename(
            title='select project.json',
            initialdir=path_uipath_projects,
            filetypes=[('project', 'project.json')]
            )
        if path_project:
            d = datetime.now()
            pr_name = f'report_{d.strftime("%Y%m%d_%H%M%S")}'
            wfa = WFA(pr_name)
            pr = wfa.run_report(path_project)
            wfa.parse_report(pr)
            # later: use threading to start second tread? or freeze app until it finishes
            del wfa
            messagebox.showinfo(message='done')
        del path_project

    def parse_json_report(self):
        path_report = fd.askopenfilename(
            title='select json report',
            filetypes=[('report', '.json')]
            )
        if path_report:
            d = datetime.now()
            pr_name = f'report_{d.strftime("%Y%m%d_%H%M%S")}'
            wfa = WFA(pr_name)
            wfa.parse_report(path_report)
            # later: use threading to start second tread? or freeze app until it finishes
            del wfa
            messagebox.showinfo(message='done')
        del path_report

    def open_reports(self):
        wfa = WFA('xd')
        subprocess.Popen(rf'explorer {wfa.path_csv_reports_dir}')

# debug app
#root = Tk()
#w = Window(root)
#w.parse_json_report()
#w.parse_json_report()

root = Tk()
app = Window(root)

root.wm_title("Workflow Analyzer handler")
root.geometry("320x200")
root.mainloop()
