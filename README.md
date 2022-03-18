# dash-uber-example

Create a compute environment with: <br /><br />
Base image: `quay.io/domino/base:Ubuntu18_DAD_Py3.8_R4.0-20210126`

Dockerfile instructions:
```
RUN pip install "plotly<4.0.0" requests "pystan==2.17.1.0" && pip install fbprophet==0.6
RUN pip install dash==1.20.0 dash-core-components==1.16.0 dash-html-components==1.1.3 dash-renderer==1.9.1 dash-table==4.11.3
RUN pip install numpy
```

