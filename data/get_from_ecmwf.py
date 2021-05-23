#!/usr/bin/env python
from ecmwfapi import ECMWFDataServer


def get_data(dates: str, steps: str, ofile: str):
    server = ECMWFDataServer()
    server.retrieve(
        {
            "class": "s2",
            "dataset": "s2s",
            "date": dates,
            "expver": "prod",
            "levtype": "sfc",
            "model": "glob",
            "origin": "ecmf",
            "param": "228141",
            "step": steps,
            "stream": "enfo",
            "time": "00:00:00",
            "type": "cf",
            "target": ofile,
            "format": "netcdf",
        }
    )
