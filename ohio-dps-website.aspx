

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head id="Head1"><meta name="googlebot" content="noindex" /><meta name="robots" content="noindex" /><title>
	Ohio Department of Public Safety
</title>        
	    <script language="javascript" src="/CrashRetrieval/Content/Scripts/menu.js" type="text/javascript"></script>
        <script language="javascript" src="/CrashRetrieval/Content/Scripts/websiteScripts.js" type="text/javascript"></script>
	    <meta name="robots" content="ALL" /><link rel="SHORTCUT ICON" href="Content/Images/favicon.ico" />
		<!-- Used by the main application -->
		<link href="Content/CSS/Styles.css" type="text/css" rel="stylesheet" />
    <style type="text/css">
        .hiddencol
        {
            display: none;
        }
        .viscol
        {
            display: block;
        }
        .uppercase
        {
            text-transform: uppercase;
        }
        .style4
        {
            width: 147px;
        }
        .style5
        {
            width: 369px;
        }
    </style>
    <script language="javascript" type="text/javascript">
        //if fips or ncic code check whether it spans across multiple counties
        function CountyConfirm() {
            if (document.getElementById("main_hdntype").value == 'fips') {
                if (document.getElementById("main_hdnCountyCount").value > 1) {
                    var retval = confirm('This FIPS Code spans across multiple counties. Do you want to download the data for all counties?.\n (Press "OK" for all counties (OR) "Cancel" for the selected county)');
                    if (!retval) {
                        document.getElementById("main_hdnCountyCount").value = 0;
                    }
                }
            }

            if (document.getElementById("main_hdntype").value == 'ncic') {
                if (document.getElementById("main_hdnCountyCount").value > 1) {
                    var retval = confirm('This NCIC Code spans across multiple counties. Do you want to download the data for all counties?.\n (Press "OK" for all counties (OR) "Cancel" for the selected county)');
                    if (!retval) {
                        document.getElementById("main_hdnCountyCount").value = 0;
                    }
                }
            }
        }

        function OpenCalendar(TextBoxID) {
            var ChildWindow;
            var Params = "width= 370,height=240,top=345, left=1225";
            var URL = "./frmCalendar.aspx?TextBoxID=" + TextBoxID;
            var Title = "CalendarPopup"
            ChildWindow = window.open(URL, Title, Params);
        }

        function GetCalendarDate(CalendarDate, TextBoxID) {
            switch (TextBoxID) {
                case 'txtCrashDate':
                    document.getElementById("main_txtCrashDate").value = CalendarDate;
                    break;
                case 'txtCrashAddDate':
                    document.getElementById("main_txtCrashAddDate").value = CalendarDate;
                    break;
            }
        }
    </script>
</head>

 <body id="defaultpage">
    <form method="post" action="./OHCrashRetrieval.aspx" id="form">
<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="vT0Msu4n6hceJ389raCZKioGeXXnGp3tRj1njJUN8SCO1Mn5PdVsE5+CYARjyLBySE707/laVKdG+K+kdVz2CKNOpgU4bjQlHJkEeiCv+x0/8Sj7l/h8HsJxNgl6q79ftC2cS/jSmcWO+M8WPJPWKiOjtbQHo6LsaS5BRAVoItOMuvxbpzubF2bkQyIyOx7/KowY9pW76nvlYt++A5qOzpUlHcZE8Mm94Nkn8E45N8foeOV9QgsOKIrNV9jtyiso6+eKFd81cRAR09Mj2QvaXUrpzCx634TlPY+W8JKFtwPDV7yI1eziON7Tne9B561rdzNf/c2EnY7caJAH3HoYmLui2MPPY7D/p973NdgLLMgzYYGgLHUVnROFEbTj3zq2C9s/sjhnymcMewnCTbEJKsKnexcVW6CALYbv1ITCjSPDdvXTpxl9LSves0biTQFv1Es6ItrVMhcwbClTKCFkR+ppzoLZYh4tmYxkbaUQ1THIgaMrlSAyz8wZM9MbCap/jJqaKR3qHZE7SjrkIXRkbaaQjXeRmXElAuYTnXy9eZgDHHikOA/Lgo5wv8nDkTFqaOIJTeeZSRsAvhTIrNn8rue/W4CZkQdfgt7IOdcEopZ5poD7hvbGid6WL3/AnEJmJ+WcM+MOCAIjto4rwM82V7bPk4zv2aQ3V05TBwxxWXIuPLWOK46jnprMfklvBYd2bngy3ypW3KKltCgPRgzq6fyfwFYEW1SC/WlJ6hODCzFuwcmjyR0jldGHir1F8LoMRa7dxC2TiQq8DSUwdOTDMnKWSBJx+6F8SEqJtn3xGWNoKGNIGBQUhZJrZVbgUY7dohI1bU3tUROOqcGDYzrBqZfFy1E8YiQfVChgNVtbKNqe416lFbFGbefwXIMYP7VL/3XbKe+Enbr7/G+hzwQvghWGHdzktP38sbazKc1w5YdLeJJ8nf+yBSSBrVeZW9V4Ntkkvg==" />

<input type="hidden" name="__VIEWSTATEGENERATOR" id="__VIEWSTATEGENERATOR" value="3A09017E" />
<input type="hidden" name="__VIEWSTATEENCRYPTED" id="__VIEWSTATEENCRYPTED" value="" />
<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="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" />
    <div>
        <div id="MasterContainer">
            <div id="Hed">
                <div id="Toplinks">
                    <a href="http://publicsafety.ohio.gov">ODPS Home</a> | <a href="../otso_aboutus.stm">
                        About Us</a> |&nbsp;<a href="http://www.publicsafety.ohio.gov/media_center.stm" target="_parent">News</a>
                    | <a href="mailto:Webmaster@dps.state.oh.us" target="_blank">Webmaster</a></div>
                <div id="LogoLeft">
                    <a id="OhioLink" href="http://www.ohio.gov" title="Ohio.gov"></a>
                </div>
                <div id="LogoRight">
                    <a id="HomeLink" href="http://publicsafety.ohio.gov" title="Ohio Department of Public Safety">
                    </a>
                </div>
                <div id="MainNav">
                    <!-- /** DROPDOWN UPDATE == START **/  -->
                    <a href="http://www.publicsafety.ohio.gov/index.stm">Home</a> | <a href="#" onclick="return clickreturnvalue()"
                        onmouseover="dropdownmenu(this, event, menu1, '240px');" onmouseout="delayhidemenu()">
                        ODPS Divisions</a> | <a href="http://www.publicsafety.ohio.gov/aboutodps.stm">About
                            ODPS</a> | <a href="http://www.publicsafety.ohio.gov/services.stm">Services</a>
                    | <a href="http://www.publicsafety.ohio.gov/media_center.stm">Media Center</a> |
                    <a href="http://www.publicsafety.ohio.gov/contacts.stm">Contact Us</a>
                    <!-- /** DROPDOWN UPDATE == END  **/ -->
                    <div class="clear">
                    </div>
                </div>
                <div id="Bottom">
                </div>
            </div>
            <div id="Content">
                
                <h1>
                    Ohio Department Of Public Safety <span>Crash Retrieval</span>
                </h1>
                
                
                
                
                
    <div>
         
                <div align="center" style="background-color:  #ebf6ff">
                    <fieldset style="border-color: #000000; width: 947px">
                        <legend style="font-family: Arial; font-size: 14px; font-weight: bold; font-style: normal;
                            font-variant: normal; color: Navy">Retrieve Ohio Crash Reports</legend>
                        <table width="947" border="0" align="center">
                            <tr>
                                <td align="left" class="style4">
                                    <span id="main_Label3">County:</span>
                                </td>
                                <td style="width: 282px" align="left">
                                    <select name="ctl00$main$cboCounty" id="main_cboCounty" tabindex="2">
	<option selected="selected" value=""></option>
	<option value="01">01 Adams</option>
	<option value="02">02 Allen</option>
	<option value="03">03 Ashland</option>
	<option value="04">04 Ashtabula</option>
	<option value="05">05 Athens</option>
	<option value="06">06 Auglaize</option>
	<option value="07">07 Belmont</option>
	<option value="08">08 Brown</option>
	<option value="09">09 Butler</option>
	<option value="10">10 Carroll</option>
	<option value="11">11 Champaign</option>
	<option value="12">12 Clark</option>
	<option value="13">13 Clermont</option>
	<option value="14">14 Clinton</option>
	<option value="15">15 Columbiana</option>
	<option value="16">16 Coshocton</option>
	<option value="17">17 Crawford</option>
	<option value="18">18 Cuyahoga</option>
	<option value="19">19 Darke</option>
	<option value="20">20 Defiance</option>
	<option value="21">21 Delaware</option>
	<option value="22">22 Erie</option>
	<option value="23">23 Fairfield</option>
	<option value="24">24 Fayette</option>
	<option value="25">25 Franklin</option>
	<option value="26">26 Fulton</option>
	<option value="27">27 Gallia</option>
	<option value="28">28 Geauga</option>
	<option value="29">29 Greene</option>
	<option value="30">30 Guernsey</option>
	<option value="31">31 Hamilton</option>
	<option value="32">32 Hancock</option>
	<option value="33">33 Hardin</option>
	<option value="34">34 Harrison</option>
	<option value="35">35 Henry</option>
	<option value="36">36 Highland</option>
	<option value="37">37 Hocking</option>
	<option value="38">38 Holmes</option>
	<option value="39">39 Huron</option>
	<option value="40">40 Jackson</option>
	<option value="41">41 Jefferson</option>
	<option value="42">42 Knox</option>
	<option value="43">43 Lake</option>
	<option value="44">44 Lawrence</option>
	<option value="45">45 Licking</option>
	<option value="46">46 Logan</option>
	<option value="47">47 Lorain</option>
	<option value="48">48 Lucas</option>
	<option value="49">49 Madison</option>
	<option value="50">50 Mahoning</option>
	<option value="51">51 Marion</option>
	<option value="52">52 Medina</option>
	<option value="53">53 Meigs</option>
	<option value="54">54 Mercer</option>
	<option value="55">55 Miami</option>
	<option value="56">56 Monroe</option>
	<option value="57">57 Montgomery</option>
	<option value="58">58 Morgan</option>
	<option value="59">59 Morrow</option>
	<option value="60">60 Muskingum</option>
	<option value="61">61 Noble</option>
	<option value="62">62 Ottawa</option>
	<option value="63">63 Paulding</option>
	<option value="64">64 Perry</option>
	<option value="65">65 Pickaway</option>
	<option value="66">66 Pike</option>
	<option value="67">67 Portage</option>
	<option value="68">68 Preble</option>
	<option value="69">69 Putnam</option>
	<option value="70">70 Richland</option>
	<option value="71">71 Ross</option>
	<option value="72">72 Sandusky</option>
	<option value="73">73 Scioto</option>
	<option value="74">74 Seneca</option>
	<option value="75">75 Shelby</option>
	<option value="76">76 Stark</option>
	<option value="77">77 Summit</option>
	<option value="78">78 Trumbull</option>
	<option value="79">79 Tuscarawas</option>
	<option value="80">80 Union</option>
	<option value="81">81 Van Wert</option>
	<option value="82">82 Vinton</option>
	<option value="83">83 Warren</option>
	<option value="84">84 Washington</option>
	<option value="85">85 Wayne</option>
	<option value="86">86 Williams</option>
	<option value="87">87 Wood</option>
	<option value="88">88 Wyandot</option>

</select>
                                </td>
                                <td style="width: 119px" align="left">
                                    <span id="main_Label2">Crash Date:</span>
                                </td>
                                <td align="left" class="style5">
                                    <input name="ctl00$main$txtCrashDate" type="text" maxlength="10" id="main_txtCrashDate" tabindex="3" />
                                    <a onclick="javascript:OpenCalendar(&#39;txtCrashDate&#39;);" id="main_lnbCalendar1" href="javascript:__doPostBack(&#39;ctl00$main$lnbCalendar1&#39;,&#39;&#39;)"><font face="Arial" color="#990000" size="1">Pick Date</font></a>
                                </td>
                            </tr>
                            <tr>
                                <td class="style4">
                                    &nbsp;
                                </td>
                                <td style="width: 282px" align="left">
                                    
                                </td>
                                <td style="width: 119px" valign="top" align="left">
                                    <span id="main_Label21">Record Add Date:</span>
                                </td>
                                <td valign="top" align="left" class="style5">
                                    <input name="ctl00$main$txtCrashAddDate" type="text" maxlength="10" id="main_txtCrashAddDate" tabindex="3" />
                                    <a onclick="javascript:OpenCalendar(&#39;txtCrashAddDate&#39;);" id="main_lnbCalendar2" href="javascript:__doPostBack(&#39;ctl00$main$lnbCalendar2&#39;,&#39;&#39;)"><font face="Arial" color="#990000" size="1">Pick Date</font></a>
                                </td>
                            </tr>
                            <tr>
                                <td class="style4">
                                </td>
                                <td style="width: 282px">
                                </td>
                                <td style="width: 119px" valign="top" align="left">
                                    <span id="main_Label10">Days:</span>
                                </td>
                                <td valign="top" align="left" class="style5">
                                    <select name="ctl00$main$cboNumberOfDays" id="main_cboNumberOfDays" tabindex="4">
	<option selected="selected" value="1">1</option>
	<option value="7">7</option>
	<option value="15">15</option>
	<option value="Month">Month</option>

</select>
                                    <span id="main_Label9"><font size="1">Number of Days.</font></span>
                                </td>
                            </tr>
                            <tr>
                                <td align="left" valign="top" class="style4">
                                    <span id="main_Label14" style="display:inline-block;">Document Number:</span>
                                    <br />
                                    <span id="main_Label18"><font size="1">Single or Multiple Input.</font></span>
                                </td>
                                <td style="width: 282px" align="left">
                                    <textarea name="ctl00$main$txtDocNo" id="main_txtDocNo" style="font-size: 10pt; width: 150px; font-family: Times New Roman;
                                        height: 70px" tabindex="5" rows="4" wrap="hard" cols="16"></textarea>
                                </td>
                                <td style="width: 119px" valign="top" align="left">
                                    <span id="main_Label17" style="display:inline-block;">Range Number:</span>
                                </td>
                                <td valign="top" align="left" class="style5">
                                    <input name="ctl00$main$txtDocNoRange" type="text" maxlength="11" id="main_txtDocNoRange" tabindex="6" />
                                </td>
                            </tr>
                        </table>
                        <table width="947" border="0" align="center">
                            <tr>
                                <td valign="middle" align="left">
                                    <div id="main_Panel2">
	
                                        <table id="Table1" bordercolor="#000080" height="130" cellspacing="3" cellpadding="0"
                                            width="200" border="0">
                                            <tr>
                                                <td style="border-right: 2px solid; border-top: 2px solid; border-left: 2px solid;
                                                    border-bottom: 2px solid; background-color: #ffff99" align="center">
                                                    <img id="main_SpoofImage" src="ShowSpoofImage.aspx?rndval=2U4XF" height="38" width="168" />
                                                    <br />
                                                    <span id="main_Label13"><b><font color="Navy" size="1">Enter the Text from the Image:</font></b></span>
                                                    <input name="ctl00$main$txtSpoofText" type="text" maxlength="6" id="main_txtSpoofText" />
                                                    <br />
                                                    
                                                </td>
                                            </tr>
                                        </table>
                                    
</div>
                                    <table>
                                    <tr>
                                        <td align="left" valign="middle">
                                            
                                        </td>
                                    </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                        <table width="947" border="0" align="center">
                            <tr>
                                <td align="left" class="style4">
                                    <span id="main_Label6">Jurisdiction:</span>
                                </td>
                                <td align="left">
                                    <select name="ctl00$main$cboFIPS" id="main_cboFIPS" tabindex="7">

</select>
                                    <span id="main_Label19"><font color="Firebrick" size="1">FIPS By County</font></span>
                                </td>
                            </tr>
                            <tr>
                                <td align="left" class="style4">
                                    <span id="main_Label5">Law Enforcement:</span>
                                </td>
                                <td align="left">
                                    <select name="ctl00$main$cboNCIC" id="main_cboNCIC" tabindex="8">

</select>
                                    <span id="main_Label20"><font color="Firebrick" size="1">NCIC By County</font></span>
                                </td>
                            </tr>
                            <tr>
                                <td align="left" class="style4">
                                    <span id="main_Label11">Last Name:</span>
                                </td>
                                <td align="left">
                                    <input name="ctl00$main$txtLastName" type="text" maxlength="25" id="main_txtLastName" tabindex="9" />
                                </td>
                            </tr>
                        </table>
                        <table width="947" border="0" align="center">
                            <tr>
                                <td align="left">
                                    <input name="ctl00$main$yCoordHolder" type="hidden" id="main_yCoordHolder" style="width: 34px; height: 22px" size="1" /><input name="ctl00$main$xCoordHolder" type="hidden" id="main_xCoordHolder" style="width: 40px;
                                            height: 22px" size="1" />
                                </td>
                                <td>
                                    <input name="ctl00$main$hdntype" type="hidden" id="main_hdntype" style="width: 40px; height: 22px" size="1" /><input name="ctl00$main$hdnCountyCount" type="hidden" id="main_hdnCountyCount" style="width: 40px; height: 22px" size="1" />
                                </td>
                                <td>
                                </td>
                            </tr>
                            <tr>
                                <td align="left">
                                    <input type="submit" name="ctl00$main$btnGetData" value="Get Report Data" onclick="javascript:CountyConfirm();" id="main_btnGetData" tabindex="10" />
                                </td>
                                <td align="left">
                                    <input type="submit" name="ctl00$main$btnHome" value="Home" id="main_btnHome" tabindex="11" />
                                </td>
                                <td align="left">
                                    <span id="main_Label12"><font size="2">Crash Report retrieval</font></span>&nbsp;<a id="main_lnkHelp" href="javascript:__doPostBack(&#39;ctl00$main$lnkHelp&#39;,&#39;&#39;)"><font size="2">help.</font></a>&nbsp;&nbsp;&nbsp;
                                    <a id="main_lnkClearMessage" href="javascript:__doPostBack(&#39;ctl00$main$lnkClearMessage&#39;,&#39;&#39;)"><font size="2">Clear Message</font></a>
                                </td>
                            </tr>
                        </table>
                        <table border="0" align="center" style="width: 935px">
                            <tr>
                                <td align="left">
                                    <span id="main_Label15"><b><u><font color="DarkRed" size="3">The crash reports provided on this site are not official documents.</font></u></b></span>
                                </td>
                            </tr>
                            <tr>
                                <td align="left">
                                    <span id="main_Label16" style="display:inline-block;"><font color="DarkRed" size="2">They were submitted to the Ohio Department of Public Safety for statistical purposes only.  Changes to a report may have been made to clarify the data prior to being entered.  If you wish to obtain the official report and the supplemental information you will need to contact the agency that investigated the crash.  These reports are to be used for statistical use only and are not sufficient to be used for any court proceeding.</font></span>
                                </td>
                            </tr>
                            <tr>
                                <td align="left">
                                    &nbsp;
                                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;
                                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                                    
                                </td>
                            </tr>
                            <tr>
                                <td align="left">
                                    <div>

</div>
                                </td>
                            </tr>
                        </table>
                    </fieldset>
                </div>
                <table width="947" border="0" align="center">
                        <tr>
                            <td align="left">
                                <input name="ctl00$main$hdSpoofValue" type="hidden" id="main_hdSpoofValue" value="2U4XF" />
                            </td>
                            <td align="left">
                                
                            </td>
                            <td align="left">
                                
                            </td>
                        </tr>
                    </table>
            
    </div>

                
                
                
            </div>
        </div>
        <div id="FooterContainer">
            <div id="Footer">
                <p>
                    <a href="http://publicsafety.ohio.gov/media_center.stm">News</a> &nbsp;|&nbsp; <a
                        href="http://publicsafety.ohio.gov/diroffice.stm">Director's Office</a> &nbsp;|&nbsp;
                    <a href="http://publicsafety.ohio.gov/privacystatement.stm">Privacy Statement</a>
                    &nbsp;|&nbsp; <a href="http://publicsafety.ohio.gov/disclaimer.stm">Disclaimer</a>
                    &nbsp;|&nbsp; <a href="http://publicsafety.ohio.gov/sitemap.stm">Site Map</a> &nbsp;|&nbsp;
                    <a href="http://careers.ohio.gov/" target="_blank">Employment</a> &nbsp;|&nbsp;
                    <a href="mailto:Webmaster@dps.state.oh.us" target="_blank">Webmaster</a> &nbsp;|&nbsp;
                    <a href="http://publicsafety.ohio.gov/contacts.stm">Contact Us</a></p>
            </div>
        </div>
    </div>
    </form>
</body>
</html>