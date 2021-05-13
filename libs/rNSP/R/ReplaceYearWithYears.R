#' Builds the node and edge datafiles from raw datafiles
#'
#' @export
#' @param year the single year value to replace with NSP time period equivelant
ReplaceYearWithYears <- function(year) {
  if (year >= 2013 & year <= 2017) {
    return("2013-2017")
  } else if (year >= 2008) {
    return("2008-2012")
  } else if (year >= 2003) {
    return("2003-2007")
  } else if (year >= 1998) {
    return("1998-2002")
  } else if (year >= 1993) {
    return("1993-1997")
  } else if (year >= 1988) {
    return("1988-1992")
  } else if (year >= 1983) {
    return("1983-1987")
  } else if (year >= 1978) {
    return("1978-1982")
  } else if (year >= 1973) {
    return("1973-1977")
  } else {
    return(NA)
  }
}
