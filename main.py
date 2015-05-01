#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import logging
from models.odoj_ip_generator import WeeklyReport
from template_base import Handler
import tools.tools as tools

class WeeklyHandler(Handler):
    def get(self):
        path = 'odoj_template/weekly.txt'
        report_template, error = tools.getFileContent(path, __file__)
        self.render("weekly.html", data={'template':report_template.decode('utf-8')})

    def post(self):
        rekap_harian = self.request.get("rekap_harian")
        template = self.request.get("template")

        if not template:
            template = getDefaultTemplate(self)
        else:
            template = template.encode('utf-8')
            if template.strip() == '':
                template = getDefaultTemplate(self)

        model = WeeklyReport(rekap_harian, template)

        rekap_pekanan = model.print_classified(template=True)
        self.render("weekly_result.html", data={'rekap_pekanan': rekap_pekanan.decode('utf-8')})

    def getDefaultTemplate(self):
        path = 'odoj_template/weekly.txt'
        template, error = tools.getFileContent(path, __file__)
        if error == '':
            return template
        else:
            raise ValueError('failed to load default template: ' + error)


app = webapp2.WSGIApplication([
    ('/odoj/weekly', WeeklyHandler)
    , ('/', WeeklyHandler)
], debug=True)
