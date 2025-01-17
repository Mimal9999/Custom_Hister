﻿using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Hister
{
    sealed class SecondsToStringConverter : IValueConverter
    {
        public object? Convert(object? value, Type targetType, object? parameter, CultureInfo culture)
        {
            if (value is not double && value is not TimeSpan)
            {
                return value;
            }

            StringBuilder formatBuilder = new();

            if (value is double doubleValue)
            {
                var timeSpan = TimeSpan.FromSeconds(doubleValue);

                if (timeSpan.Hours > 0)
                {
                    formatBuilder.Append(@"hh\:");
                }

                formatBuilder.Append(@"mm\:ss");

                return timeSpan.ToString(formatBuilder.ToString());
            }
            else if (value is TimeSpan timespanValue)
            {
                if (timespanValue.Hours > 0)
                {
                    formatBuilder.Append(@"hh\:");
                }

                formatBuilder.Append(@"mm\:ss");

                return timespanValue.ToString(formatBuilder.ToString());
            }

            return value;
        }

        public object? ConvertBack(object? value, Type targetType, object? parameter, CultureInfo culture)
        {
            throw new NotSupportedException();
        }
    }
}
