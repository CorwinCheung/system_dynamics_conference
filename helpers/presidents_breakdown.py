from collections import Counter
import re

list_of_presidents = """2023 - Shayne Gary - University of New South Wales - Australia
2022 - J. Bradley Morrison - Brandeis University - United States of America
2021 - Paulo Gonclaves - University of Lugano - Switzerland
2020 - Birgit Kopainsky - University of Bergen - Norway
2019 - Martin F. G. Schaffernicht - Universidad de Talca - Chile
2018 - I. Martínez Moyano - Argonne National Laboratory - United States of America
2017 - Leonard Malczynski - Sandia National Laboratories - United States of America
2016 - Etiënne A.J.A. Rouwette - Radboud University - The Netherlands
2015 - Jürgen Strohhecker - Frankfurt School of Finance and Management - Germany
2014 - Edward G. Anderson - University of Texas - United States of America
2013 - Kim Warren - London Business School - United Kingdom
2012 - David Ford - Texas A&M University - United States of America
2011 - David Lane - London School of Economics - United Kingdom
2010 - Rogelio Oliva - Texas A&M University - United States of America
2009 - Erling Moxnes - University of Bergen - Norway
2008 - James M. Lyneis - Worcester Polytechnic Institute - United States of America
2007 - Qifan Wang - Huazhong University of Science and Technology - China
2006 - Michael J. Radzicki - Worcester Polytechnic Institute - United States of America
2005 - Graham Winch - University of Plymouth - United Kingdom
2004 - Robert Eberlein - Worcester Polytechnic Institute - United States of America
2003 - Pål I. Davidsen - University of Bergen - Norway
2002 - James H. Hines, Jr. - Massachusetts Institute of Technology - United States of America
2001 - Ali N. Mashayekhi - Sharif University of Technology - Iran
2000 - Jac A. M. Vennix - Radboud University - The Netherlands
1999 - Alexander L. Pugh, III - PughRoberts Associates - United States of America
1998 - Yaman Barlas - Bogazici University - Turkey
1997 - George P. Richardson - State University of New York at Albany - United States of America
1996 - John D. W. Morecroft - London Business School - United Kingdom
1995 - Khalid Saeed - Asian Institute of Technology - Thailand
1994 - Andrew Ford - Washington State University - United States of America
1993 - Peter M. Milling - University of Stuttgart - Germany
1992 - John D. Sterman - Massachusetts Institute of Technology - United States of America
1991 - Erich K. O. Zahn - University of Stuttgart - Germany
1990 - Peter Gardiner - University of Southern California - United States of America
1989 - Eric F. Wolstenholme - University of Bradford - United Kingdom
1988 - Nathan B. Forrester - Massachusetts Institute of Technology - United States of America
1987 - Dennis L. Meadows - Dartmouth College - United States of America
1986 - Jørgen Randers - Ministry of LongTerm Planning - Norway
1985 - David F. Andersen - State University of New York at Albany - United States of America
1984 - Jay W. Forrester - Massachusetts Institute of Technology - United States of America"""

def main():
    print("hello world")
    items = re.split(r"[-\n]",list_of_presidents)
    year = []
    name = []
    college = []
    country = []



    print(len(items))

    for i in range(len(items)):
        if i % 4 == 0:
            year.append(items[i])
        elif i % 4 == 1:
            name.append(items[i])
        elif i % 4 == 2:
            college.append(items[i])
        else:
            country.append(items[i])


    year = [s.strip() for s in year]
    name = [s.strip() for s in name]
    college = [s.strip() for s in college]
    country = [s.strip() for s in country]


    counts_college = Counter(college)
    college_dict = dict(counts_college)
    college_dict = sorted(college_dict.items(),key=lambda x:x[1],reverse=True)

    counts_country = Counter(country)
    country_dict = dict(counts_country)
    country_dict = sorted(country_dict.items(),key=lambda x:x[1],reverse=True)


    print("Years")
    print(year)

    print("Names")
    print(name)

    print("Colleges")
    print(college_dict)

    print("Country")
    print(country_dict)



main()